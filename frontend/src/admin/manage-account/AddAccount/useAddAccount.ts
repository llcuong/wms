import { Dispatch, useCallback, useEffect, useState } from "react";

import { CreateAccountData } from "@manage-account/types";
import axiosClient from "@modules/api";

interface useAddAccountProps {
    userId: string;
    setIsOpen: Dispatch<React.SetStateAction<boolean>>;
    setUserId: Dispatch<React.SetStateAction<string>>;
    getUserList: () => Promise<void>;
};

export default function useAddAccount({ userId, setIsOpen, setUserId, getUserList }: useAddAccountProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState<CreateAccountData>({
        user_id: userId,
        account_id: "",
        password: "",
    });

    useEffect(() => {
        setFormData((prev) => ({ ...prev, user_id: userId }));
    }, [userId]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setIsLoading(true);
            await axiosClient.post("/user/post-create-account/", formData);
            setIsOpen(false);
            setUserId("");
            getUserList();
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Failed to add account";
            alert(errorMessage);
        } finally {
            setIsLoading(false);
        };
    }, [formData, setIsOpen, setUserId, getUserList]);

    return {
        formData,
        isLoading,
        handleSubmit,
        handleChange,
    };
};