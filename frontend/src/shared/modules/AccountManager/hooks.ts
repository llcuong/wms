import { useState, useEffect, useCallback } from "react";
import { accountManagerAPI } from "./api";
import type { User, Account, UserStatus, CreateUserPayload, UpdateUserPayload, CreateAccountPayload } from "./types";

export function useUsers() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchUsers = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await accountManagerAPI.getUsers();
            setUsers(data);
        } catch (err) {
            setError("Failed to fetch users");
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []);

    const createUser = useCallback(async (payload: CreateUserPayload) => {
        const newUser = await accountManagerAPI.createUser(payload);
        setUsers(prev => [...prev, newUser]);
        return newUser;
    }, []);

    const updateUser = useCallback(async (id: number, payload: UpdateUserPayload) => {
        const updated = await accountManagerAPI.updateUser(id, payload);
        setUsers(prev => prev.map(u => u.id === id ? updated : u));
        return updated;
    }, []);

    const deleteUser = useCallback(async (id: number) => {
        await accountManagerAPI.deleteUser(id);
        setUsers(prev => prev.filter(u => u.id !== id));
    }, []);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    return {
        users,
        loading,
        error,
        refetch: fetchUsers,
        createUser,
        updateUser,
        deleteUser
    };
}

export function useAccounts() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchAccounts = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await accountManagerAPI.getAccounts();
            setAccounts(data);
        } catch (err) {
            setError("Failed to fetch accounts");
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, []);

    const createAccount = useCallback(async (payload: CreateAccountPayload) => {
        const newAccount = await accountManagerAPI.createAccount(payload);
        setAccounts(prev => [...prev, newAccount]);
        return newAccount;
    }, []);

    const deleteAccount = useCallback(async (id: number) => {
        await accountManagerAPI.deleteAccount(id);
        setAccounts(prev => prev.filter(a => a.id !== id));
    }, []);

    const resetPassword = useCallback(async (id: number, password: string) => {
        await accountManagerAPI.resetPassword(id, password);
    }, []);

    useEffect(() => {
        fetchAccounts();
    }, [fetchAccounts]);

    return {
        accounts,
        loading,
        error,
        refetch: fetchAccounts,
        createAccount,
        deleteAccount,
        resetPassword
    };
}

export function useUserStatuses() {
    const [statuses, setStatuses] = useState<UserStatus[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        accountManagerAPI.getUserStatuses()
            .then(setStatuses)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    return { statuses, loading };
}
