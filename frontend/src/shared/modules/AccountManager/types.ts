// Types for User and Account management

export interface UserStatus {
    status_id: number;
    status_name: string;
}

export interface User {
    id?: number;
    user_id: string;
    user_name: string;
    user_full_name: string;
    user_email?: string;
    user_status?: UserStatus;
    user_account?: {
        account_id: string;
    };
    created_at?: string;
    updated_at?: string;
}

export interface Account {
    id?: number;
    user_id: string;
    account_id: string;
    account_last_login?: string;
    account_role?: string;
    created_at?: string;
}

export interface CreateUserPayload {
    user_id: string;
    user_name: string;
    user_full_name: string;
    user_email?: string;
    user_status_id: number;
}

export interface UpdateUserPayload {
    user_name?: string;
    user_full_name?: string;
    user_email?: string;
    user_status_id?: number;
}

export interface CreateAccountPayload {
    user_id: string;
    account_id: string;
    password: string;
}

export interface UpdateAccountPayload {
    account_id?: string;
}
