import axiosClient from '../api';

export interface LoginRequest {
    account_id: string;
    password: string;
}

export interface LoginResponse {
    user_id: string;
    account_id: string;
    user_name: string;
    user_full_name: string;
    user_email: string;
    token: string;
    last_login: string;
}

export const authAPI = {
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
        const response = await axiosClient.post<LoginResponse>('/user/login/', credentials);
        return response.data;
    },

    logout: async (): Promise<void> => {
        await axiosClient.post('/user/logout/');
    }
};