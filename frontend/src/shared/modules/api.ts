import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from './Authentication/useAuthStore';

const API_BASE_URL = 'http://172.18.55.215:10000';

const axiosClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
    withCredentials: true,
});

let isRefreshing = false;
let failedQueue: Array<{
    resolve: (token: string) => void;
    reject: (error: AxiosError) => void;
}> = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
    failedQueue.forEach((prom) => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token!);
        }
    });
    failedQueue = [];
};

axiosClient.interceptors.request.use(
    (config) => {
        const token = useAuthStore.getState().token;
        if (token && config.headers) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

axiosClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

        if (error.response?.status !== 401 || originalRequest._retry) {
            return Promise.reject(error);
        }

        if (isRefreshing) {
            return new Promise((resolve, reject) => {
                failedQueue.push({ resolve, reject });
            })
                .then((token) => {
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                    return axiosClient(originalRequest);
                })
                .catch((err) => Promise.reject(err));
        }

        originalRequest._retry = true;
        isRefreshing = true;

        try {
            const response = await axios.post(
                `${API_BASE_URL}/user/post-refresh-access-token/`,
                {},
                {
                    withCredentials: true,
                    headers: {
                        'Authorization': `Bearer ${useAuthStore.getState().token}`
                    }
                }
            );

            const newAccessToken = response.data.access_token;

            const currentUser = useAuthStore.getState().user;
            if (currentUser) {
                useAuthStore.getState().login(currentUser, newAccessToken);
            }

            processQueue(null, newAccessToken);

            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return axiosClient(originalRequest);

        } catch (refreshError) {
            processQueue(refreshError as AxiosError, null);
            useAuthStore.getState().logout();

            window.location.href = '/login';

            return Promise.reject(refreshError);
        } finally {
            isRefreshing = false;
        }
    }
);

export default axiosClient;