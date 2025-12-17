const API_BASE_URL = 'http://127.0.0.1:8000';

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

export interface ApiError {
    error: string;
    message: string;
    details?: any;
}

class AuthAPI {
    private baseUrl: string;

    constructor() {
        this.baseUrl = `${API_BASE_URL}/api/auth`;
    }

    async login(credentials: LoginRequest): Promise<LoginResponse> {
        try {
            const response = await fetch(`${this.baseUrl}/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            });

            const data = await response.json();

            if (!response.ok) {
                throw {
                    error: data.error || 'Login failed',
                    message: data.message || 'An error occurred during login',
                    details: data.details,
                } as ApiError;
            }

            return data as LoginResponse;
        } catch (error) {
            if ((error as ApiError).error) {
                throw error;
            }
            throw {
                error: 'Network Error',
                message: 'Unable to connect to server. Please check your connection.',
            } as ApiError;
        }
    }

    async logout(): Promise<void> {
        try {
            const response = await fetch(`${this.baseUrl}/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('Logout error:', error);
        }
    }
}

export const authAPI = new AuthAPI();
