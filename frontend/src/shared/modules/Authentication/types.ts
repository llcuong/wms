import { ReactNode } from "react";

export interface ProtectedProps {
    children: ReactNode;
}

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
    access_token: string;
    token_type: string;
    expires_in: number;
    last_login: string;
}


export interface User {
    id: string;
    username: string;
    name: string;
    fullName: string;
    email: string;
    role?: string;
}

export interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    login: (user: User, token: string) => void;
    logout: () => void;
}
