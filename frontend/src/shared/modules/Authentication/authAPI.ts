import axiosClient from '../api';
import type { LoginRequest, LoginResponse } from './types';

export const authAPI = {
    login: async (credentials: LoginRequest): Promise<LoginResponse> => {
        const response = await axiosClient.post<LoginResponse>('/user/login/', credentials);
        return response.data;
    },

    logout: async (): Promise<void> => {
        await axiosClient.post('/user/logout/');
    }
};