import axios from 'axios';
import { useAuthStore } from './Authentication/useAuthStore';

const API_BASE_URL = 'http://172.18.55.215:10000';
const DEV_API_BASE_URL = 'http://localhost:8000';

const axiosClient = axios.create({
    baseURL: DEV_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 1000,
});

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
    (error) => {
        if (error.response && error.response.status === 401) {
            useAuthStore.getState().logout();
        }
        return Promise.reject(error);
    }
);

export default axiosClient;