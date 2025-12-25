import { Dispatch, useCallback, useState } from "react";

import { CreateUserData } from "@manage-account/types";
import axiosClient from "@modules/api";

interface useAddUserProps {
    setIsOpen: Dispatch<React.SetStateAction<boolean>>;
    getUserList: () => Promise<void>;
};

export default function useAddUser({ setIsOpen, getUserList }: useAddUserProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState<CreateUserData>({
        user_id: "",
        user_name: "",
        user_full_name: "",
        user_email: "",
        user_status_id: 1,
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = useCallback(async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setIsLoading(true);
            await axiosClient.post("/user/post-create-user/", formData);
            setIsOpen(false);
            getUserList();
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Failed to add user";
            alert(errorMessage);
        } finally {
            setIsLoading(false);
        };
    }, [formData, getUserList, setIsOpen]);

    return {
        formData,
        isLoading,
        handleSubmit,
        handleChange,
    };
};