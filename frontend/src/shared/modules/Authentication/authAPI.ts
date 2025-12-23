import axiosClient from '../api';
import type { LoginRequest, LoginResponse } from './types';

export const authAPI = {
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
        const response = await axiosClient.post<LoginResponse>('/user/post-login-account/', credentials);
        return response.data;
    },

    logout: async (): Promise<void> => {
        await axiosClient.post('/user/post-logout-account/');
    }
};