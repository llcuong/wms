import axiosClient from "../api";
import type {
    User,
    Account,
    UserStatus,
    CreateUserPayload,
    UpdateUserPayload,
    CreateAccountPayload,
    UpdateAccountPayload
} from "./types";

const API_PREFIX = "/user";

export const accountManagerAPI = {
    // ============== USER STATUS ==============
    getUserStatuses: async (): Promise<UserStatus[]> => {
        const response = await axiosClient.get(`${API_PREFIX}/statuses/`);
        return response.data;
    },

    // ============== USERS ==============
    getUsers: async (): Promise<User[]> => {
        const response = await axiosClient.get(`${API_PREFIX}/users/`);
        return response.data;
    },

    getUser: async (id: number): Promise<User> => {
        const response = await axiosClient.get(`${API_PREFIX}/users/${id}/`);
        return response.data;
    },

    createUser: async (payload: CreateUserPayload): Promise<User> => {
        const response = await axiosClient.post(`${API_PREFIX}/users/`, payload);
        return response.data;
    },

    updateUser: async (id: number, payload: UpdateUserPayload): Promise<User> => {
        const response = await axiosClient.put(`${API_PREFIX}/users/${id}/`, payload);
        return response.data;
    },

    deleteUser: async (id: number): Promise<void> => {
        await axiosClient.delete(`${API_PREFIX}/users/${id}/`);
    },

    // ============== ACCOUNTS ==============
    getAccounts: async (): Promise<Account[]> => {
        const response = await axiosClient.get(`${API_PREFIX}/accounts/`);
        return response.data;
    },

    getAccount: async (id: number): Promise<Account> => {
        const response = await axiosClient.get(`${API_PREFIX}/accounts/${id}/`);
        return response.data;
    },

    createAccount: async (payload: CreateAccountPayload): Promise<Account> => {
        const response = await axiosClient.post(`${API_PREFIX}/accounts/`, payload);
        return response.data;
    },

    updateAccount: async (id: number, payload: UpdateAccountPayload): Promise<Account> => {
        const response = await axiosClient.put(`${API_PREFIX}/accounts/${id}/`, payload);
        return response.data;
    },

    deleteAccount: async (id: number): Promise<void> => {
        await axiosClient.delete(`${API_PREFIX}/accounts/${id}/`);
    },

    resetPassword: async (id: number, password: string): Promise<void> => {
        await axiosClient.post(`${API_PREFIX}/accounts/${id}/reset-password/`, { password });
    }
};
