export interface UserAccount {
    account_id: string;
    account_last_login: string | null;
    created_at: string;
};

export interface User {
    id: number;
    user_id: string;
    user_name: string;
    user_full_name: string;
    user_email: string | null;
    user_status_name: string;
    has_account: boolean;
    account: UserAccount | null;
    created_at: string;
    updated_at: string;
};

export interface CreateUserData {
    user_id: string;
    user_name: string;
    user_full_name: string;
    user_email: string;
    user_status_id: number;
};

export interface CreateAccountData {
    user_id: string;
    account_id: string;
    password: string;
};