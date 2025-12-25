import { useCallback, useEffect, useState } from "react";

import { User } from "./types";

import axiosClient from "@modules/api";

export default function useManageAccount() {
    const [users, setUsers] = useState<User[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isAddUserModalOpen, setIsAddUserModalOpen] = useState(false);
    const [isAddAccountModalOpen, setIsAddAccountModalOpen] = useState(false);
    const [selectedUserId, setSelectedUserId] = useState("");

    const getUserList = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await axiosClient.get("/user/get-user-list/");
            setUsers(response.data);
            setError(null);
        } catch (error: unknown) {
            const errorMessage = error instanceof Error ? error.message : "Failed to fetch users";
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        };
    }, []);

    useEffect(() => {
        getUserList();
    }, [getUserList]);

    const openCreateAccountModal = useCallback((userId: string) => {
        setSelectedUserId(userId);
        setIsAddAccountModalOpen(true);
    }, []);

    return {
        users,
        isLoading,
        error,
        isAddUserModalOpen,
        isAddAccountModalOpen,
        selectedUserId,

        setIsAddUserModalOpen,
        setIsAddAccountModalOpen,
        setSelectedUserId,
        getUserList,
        openCreateAccountModal,
    };
};