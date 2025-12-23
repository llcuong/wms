import { Base } from "./Base";
import type { PageNavigatorComponent } from "@routes/types";
import { useState, useEffect, useCallback } from "react";
import axiosClient from "@modules/api";

// Types
interface UserAccount {
    account_id: string;
    account_last_login: string | null;
    created_at: string;
}

interface User {
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
}

// Modal Component for Add User
interface AddUserModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (data: CreateUserData) => void;
    isLoading: boolean;
}

interface CreateUserData {
    user_id: string;
    user_name: string;
    user_full_name: string;
    user_email: string;
    user_status_id: number;
}

const AddUserModal = ({ isOpen, onClose, onSubmit, isLoading }: AddUserModalProps) => {
    const [formData, setFormData] = useState<CreateUserData>({
        user_id: "",
        user_name: "",
        user_full_name: "",
        user_email: "",
        user_status_id: 1,
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                {/* Header */}
                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4">
                    <h2 className="text-xl font-bold text-white">Add New User</h2>
                    <p className="text-indigo-100 text-sm mt-1">Fill in the user information below</p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            User ID <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            required
                            value={formData.user_id}
                            onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                            placeholder="e.g., USER001"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Username <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            required
                            value={formData.user_name}
                            onChange={(e) => setFormData({ ...formData, user_name: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                            placeholder="e.g., johndoe"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Full Name <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            required
                            value={formData.user_full_name}
                            onChange={(e) => setFormData({ ...formData, user_full_name: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                            placeholder="e.g., John Doe"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Email
                        </label>
                        <input
                            type="email"
                            value={formData.user_email}
                            onChange={(e) => setFormData({ ...formData, user_email: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                            placeholder="e.g., john@example.com"
                        />
                    </div>

                    <div className="flex justify-end gap-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-5 py-2.5 text-gray-700 bg-gray-100 rounded-xl hover:bg-gray-200 transition-all font-medium"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all font-medium disabled:opacity-50"
                        >
                            {isLoading ? "Creating..." : "Create User"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

interface CreateAccountModalProps {
    isOpen: boolean;
    onClose: () => void;
    onSubmit: (data: CreateAccountData) => void;
    userId: string;
    isLoading: boolean;
}

interface CreateAccountData {
    user_id: string;
    account_id: string;
    password: string;
}

const CreateAccountModal = ({ isOpen, onClose, onSubmit, userId, isLoading }: CreateAccountModalProps) => {
    const [formData, setFormData] = useState<CreateAccountData>({
        user_id: userId,
        account_id: "",
        password: "",
    });

    useEffect(() => {
        setFormData((prev) => ({ ...prev, user_id: userId }));
    }, [userId]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formData);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-4">
                    <h2 className="text-xl font-bold text-white">Create Account</h2>
                    <p className="text-emerald-100 text-sm mt-1">Create login account for user: <strong>{userId}</strong></p>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Account ID <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            required
                            value={formData.account_id}
                            onChange={(e) => setFormData({ ...formData, account_id: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                            placeholder="e.g., john.doe"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Password <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="password"
                            required
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            className="w-full px-4 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                            placeholder="Enter secure password"
                        />
                    </div>

                    <div className="flex justify-end gap-3 pt-4">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-5 py-2.5 text-gray-700 bg-gray-100 rounded-xl hover:bg-gray-200 transition-all font-medium"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="px-5 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-xl hover:from-emerald-700 hover:to-teal-700 transition-all font-medium disabled:opacity-50"
                        >
                            {isLoading ? "Creating..." : "Create Account"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

const formatDate = (dateString: string | null): string => {
    if (!dateString) return "—";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

const Index: PageNavigatorComponent = (props) => {
    const [users, setUsers] = useState<User[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isAddUserModalOpen, setIsAddUserModalOpen] = useState(false);
    const [isCreateAccountModalOpen, setIsCreateAccountModalOpen] = useState(false);
    const [selectedUserId, setSelectedUserId] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fetchUsers = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await axiosClient.get("/user/get-user-list/");
            setUsers(response.data);
            setError(null);
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Failed to fetch users";
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUsers();
    }, [fetchUsers]);

    const handleCreateUser = async (data: CreateUserData) => {
        try {
            setIsSubmitting(true);
            await axiosClient.post("/user/post-create-user/", data);
            setIsAddUserModalOpen(false);
            fetchUsers();
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Failed to create user";
            alert(errorMessage);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleCreateAccount = async (data: CreateAccountData) => {
        try {
            setIsSubmitting(true);
            await axiosClient.post("/user/post-create-account/", data);
            setIsCreateAccountModalOpen(false);
            fetchUsers();
        } catch (err: unknown) {
            const errorMessage = err instanceof Error ? err.message : "Failed to create account";
            alert(errorMessage);
        } finally {
            setIsSubmitting(false);
        }
    };

    const openCreateAccountModal = (userId: string) => {
        setSelectedUserId(userId);
        setIsCreateAccountModalOpen(true);
    };

    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}
        >
            <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
                <div className="container mx-auto px-4 py-8">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                                User Management
                            </h1>
                            <p className="text-gray-500 mt-1">Manage users and their accounts</p>
                        </div>
                        <button
                            onClick={() => setIsAddUserModalOpen(true)}
                            className="group flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40"
                        >
                            <svg
                                className="w-5 h-5 group-hover:scale-110 transition-transform"
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                                />
                            </svg>
                            <span className="font-medium">Add User</span>
                        </button>
                    </div>

                    {/* Content */}
                    {isLoading ? (
                        <div className="flex items-center justify-center py-20">
                            <div className="flex flex-col items-center gap-4">
                                <div className="w-12 h-12 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin"></div>
                                <p className="text-gray-500 font-medium">Loading users...</p>
                            </div>
                        </div>
                    ) : error ? (
                        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
                            <div className="text-red-600 font-medium">{error}</div>
                            <button
                                onClick={fetchUsers}
                                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all"
                            >
                                Retry
                            </button>
                        </div>
                    ) : (
                        <div className="bg-white rounded-2xl shadow-xl shadow-gray-200/50 overflow-hidden border border-gray-100">
                            {/* Table */}
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className="bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
                                            <th className="text-left px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                User Info
                                            </th>
                                            <th className="text-left px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                Email
                                            </th>
                                            <th className="text-left px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                Status
                                            </th>
                                            <th className="text-left px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                Account ID
                                            </th>
                                            <th className="text-left px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                Last Login
                                            </th>
                                            <th className="text-right px-6 py-4 text-xs font-semibold text-gray-600 uppercase tracking-wider">
                                                Actions
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100">
                                        {users.length === 0 ? (
                                            <tr>
                                                <td colSpan={6} className="px-6 py-16 text-center">
                                                    <div className="flex flex-col items-center gap-3">
                                                        <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
                                                            <svg
                                                                className="w-8 h-8 text-gray-400"
                                                                fill="none"
                                                                stroke="currentColor"
                                                                viewBox="0 0 24 24"
                                                            >
                                                                <path
                                                                    strokeLinecap="round"
                                                                    strokeLinejoin="round"
                                                                    strokeWidth={1.5}
                                                                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"
                                                                />
                                                            </svg>
                                                        </div>
                                                        <p className="text-gray-500 font-medium">No users found</p>
                                                        <p className="text-gray-400 text-sm">
                                                            Click "Add User" to create your first user
                                                        </p>
                                                    </div>
                                                </td>
                                            </tr>
                                        ) : (
                                            users.map((user) => (
                                                <tr
                                                    key={user.id}
                                                    className="hover:bg-gray-50/50 transition-colors"
                                                >
                                                    <td className="px-6 py-4">
                                                        <div className="flex items-center gap-3">
                                                            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold text-sm shadow-lg shadow-indigo-500/25">
                                                                {user.user_full_name.charAt(0).toUpperCase()}
                                                            </div>
                                                            <div>
                                                                <div className="font-semibold text-gray-900">
                                                                    {user.user_full_name}
                                                                </div>
                                                                <div className="text-sm text-gray-500">
                                                                    <span className="font-mono bg-gray-100 px-1.5 py-0.5 rounded text-xs">
                                                                        {user.user_id}
                                                                    </span>
                                                                    <span className="mx-1">•</span>
                                                                    <span>@{user.user_name}</span>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </td>

                                                    {/* Email */}
                                                    <td className="px-6 py-4">
                                                        <span className="text-gray-600">
                                                            {user.user_email || "—"}
                                                        </span>
                                                    </td>

                                                    {/* Status */}
                                                    <td className="px-6 py-4">
                                                        <span
                                                            className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${user.user_status_name.toLowerCase() === "active"
                                                                    ? "bg-emerald-100 text-emerald-700"
                                                                    : "bg-gray-100 text-gray-600"
                                                                }`}
                                                        >
                                                            <span
                                                                className={`w-1.5 h-1.5 rounded-full mr-1.5 ${user.user_status_name.toLowerCase() === "active"
                                                                        ? "bg-emerald-500"
                                                                        : "bg-gray-400"
                                                                    }`}
                                                            ></span>
                                                            {user.user_status_name}
                                                        </span>
                                                    </td>

                                                    {/* Account ID */}
                                                    <td className="px-6 py-4">
                                                        {user.has_account && user.account ? (
                                                            <span className="font-mono text-sm bg-indigo-50 text-indigo-700 px-2 py-1 rounded">
                                                                {user.account.account_id}
                                                            </span>
                                                        ) : (
                                                            <span className="text-gray-400 italic">
                                                                No account
                                                            </span>
                                                        )}
                                                    </td>

                                                    {/* Last Login */}
                                                    <td className="px-6 py-4">
                                                        <span className="text-sm text-gray-500">
                                                            {user.account
                                                                ? formatDate(user.account.account_last_login)
                                                                : "—"}
                                                        </span>
                                                    </td>

                                                    <td className="px-6 py-4 text-right">
                                                        {user.has_account ? (
                                                            <button className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-indigo-600 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-all">
                                                                <svg
                                                                    className="w-4 h-4"
                                                                    fill="none"
                                                                    stroke="currentColor"
                                                                    viewBox="0 0 24 24"
                                                                >
                                                                    <path
                                                                        strokeLinecap="round"
                                                                        strokeLinejoin="round"
                                                                        strokeWidth={2}
                                                                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                                                                    />
                                                                </svg>
                                                                Edit
                                                            </button>
                                                        ) : (
                                                            <button
                                                                onClick={() => openCreateAccountModal(user.user_id)}
                                                                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-emerald-600 bg-emerald-50 rounded-lg hover:bg-emerald-100 transition-all"
                                                            >
                                                                <svg
                                                                    className="w-4 h-4"
                                                                    fill="none"
                                                                    stroke="currentColor"
                                                                    viewBox="0 0 24 24"
                                                                >
                                                                    <path
                                                                        strokeLinecap="round"
                                                                        strokeLinejoin="round"
                                                                        strokeWidth={2}
                                                                        d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                                                                    />
                                                                </svg>
                                                                Create Account
                                                            </button>
                                                        )}
                                                    </td>
                                                </tr>
                                            ))
                                        )}
                                    </tbody>
                                </table>
                            </div>

                            {/* Footer */}
                            {users.length > 0 && (
                                <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
                                    <p className="text-sm text-gray-500">
                                        Showing <span className="font-medium text-gray-900">{users.length}</span> users
                                    </p>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <AddUserModal
                isOpen={isAddUserModalOpen}
                onClose={() => setIsAddUserModalOpen(false)}
                onSubmit={handleCreateUser}
                isLoading={isSubmitting}
            />
            <CreateAccountModal
                isOpen={isCreateAccountModalOpen}
                onClose={() => setIsCreateAccountModalOpen(false)}
                onSubmit={handleCreateAccount}
                userId={selectedUserId}
                isLoading={isSubmitting}
            />
        </Base>
    );
};

export default Index;