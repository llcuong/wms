import { useState, FC } from 'react';
import { useAccounts, useUsers } from './hooks';
import type { Account, CreateAccountPayload } from './types';
import { accountManagerAPI } from './api';

interface AccountFormData {
    user_id: string;
    account_id: string;
    password: string;
}

const initialFormData: AccountFormData = {
    user_id: '',
    account_id: '',
    password: '',
};

export const AccountManager: FC = () => {
    const { accounts, loading, error, refetch, createAccount, deleteAccount } = useAccounts();
    const { users } = useUsers();

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isResetPasswordOpen, setIsResetPasswordOpen] = useState(false);
    const [selectedAccount, setSelectedAccount] = useState<Account | null>(null);
    const [formData, setFormData] = useState<AccountFormData>(initialFormData);
    const [newPassword, setNewPassword] = useState('');
    const [submitError, setSubmitError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Get users without accounts for the dropdown
    const usersWithoutAccounts = users.filter(user => !user.user_account);

    const handleOpenCreate = () => {
        setFormData(initialFormData);
        setSubmitError(null);
        setIsModalOpen(true);
    };

    const handleOpenResetPassword = (account: Account) => {
        setSelectedAccount(account);
        setNewPassword('');
        setSubmitError(null);
        setIsResetPasswordOpen(true);
    };

    const handleClose = () => {
        setIsModalOpen(false);
        setIsResetPasswordOpen(false);
        setSelectedAccount(null);
        setFormData(initialFormData);
        setNewPassword('');
        setSubmitError(null);
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const payload: CreateAccountPayload = {
                user_id: formData.user_id,
                account_id: formData.account_id,
                password: formData.password,
            };
            await createAccount(payload);
            handleClose();
            refetch();
        } catch (err) {
            setSubmitError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleResetPassword = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedAccount?.id) return;

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await accountManagerAPI.resetPassword(selectedAccount.id, newPassword);
            handleClose();
            alert('Password has been reset successfully!');
        } catch (err) {
            setSubmitError(err instanceof Error ? err.message : 'Failed to reset password');
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleDelete = async (account: Account) => {
        if (!confirm(`Are you sure you want to delete account "${account.account_id}"?`)) return;

        try {
            await deleteAccount(account.id!);
            refetch();
        } catch (err) {
            alert(err instanceof Error ? err.message : 'Failed to delete account');
        }
    };

    const formatDate = (dateString?: string) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleString();
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-600">{error}</p>
                <button onClick={refetch} className="mt-2 text-red-700 underline">
                    Try again
                </button>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-4">
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-xl font-bold text-white">Account Management</h2>
                        <p className="text-emerald-100 text-sm mt-1">Manage user login accounts</p>
                    </div>
                    <button
                        onClick={handleOpenCreate}
                        disabled={usersWithoutAccounts.length === 0}
                        className="bg-white text-emerald-600 px-4 py-2 rounded-lg font-medium hover:bg-emerald-50 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        Add Account
                    </button>
                </div>
            </div>

            {/* Table */}
            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Account ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Login</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {accounts.map((account) => (
                            <tr key={account.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    <div className="flex items-center gap-2">
                                        <div className="w-8 h-8 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                                            {account.account_id.charAt(0).toUpperCase()}
                                        </div>
                                        {account.account_id}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                                    {account.user_id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                        {account.account_role || 'User'}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {formatDate(account.account_last_login)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {formatDate(account.created_at)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <button
                                        onClick={() => handleOpenResetPassword(account)}
                                        className="text-amber-600 hover:text-amber-900 mr-3 transition-colors"
                                    >
                                        Reset Password
                                    </button>
                                    <button
                                        onClick={() => handleDelete(account)}
                                        className="text-red-600 hover:text-red-900 transition-colors"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {accounts.length === 0 && (
                    <div className="text-center py-12">
                        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                        </svg>
                        <h3 className="mt-2 text-sm font-medium text-gray-900">No accounts</h3>
                        <p className="mt-1 text-sm text-gray-500">Get started by creating a new account.</p>
                    </div>
                )}
            </div>

            {/* Create Account Modal */}
            {isModalOpen && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full transform transition-all">
                        <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-6 py-4 rounded-t-2xl">
                            <h3 className="text-lg font-semibold text-white">Create New Account</h3>
                        </div>

                        <form onSubmit={handleSubmit} className="p-6 space-y-4">
                            {submitError && (
                                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                                    {submitError}
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Select User</label>
                                <select
                                    name="user_id"
                                    value={formData.user_id}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                                >
                                    <option value="">-- Select a user --</option>
                                    {usersWithoutAccounts.map((user) => (
                                        <option key={user.user_id} value={user.user_id}>
                                            {user.user_id} - {user.user_full_name}
                                        </option>
                                    ))}
                                </select>
                                {usersWithoutAccounts.length === 0 && (
                                    <p className="mt-1 text-sm text-amber-600">All users already have accounts</p>
                                )}
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Account ID (Login username)</label>
                                <input
                                    type="text"
                                    name="account_id"
                                    value={formData.account_id}
                                    onChange={handleInputChange}
                                    required
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                                    placeholder="Enter account ID"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleInputChange}
                                    required
                                    minLength={6}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
                                    placeholder="Enter password (min 6 characters)"
                                />
                            </div>

                            <div className="flex justify-end gap-3 pt-4">
                                <button
                                    type="button"
                                    onClick={handleClose}
                                    className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                                >
                                    {isSubmitting && (
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                    )}
                                    Create Account
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Reset Password Modal */}
            {isResetPasswordOpen && selectedAccount && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full transform transition-all">
                        <div className="bg-gradient-to-r from-amber-500 to-orange-500 px-6 py-4 rounded-t-2xl">
                            <h3 className="text-lg font-semibold text-white">Reset Password</h3>
                            <p className="text-amber-100 text-sm">Account: {selectedAccount.account_id}</p>
                        </div>

                        <form onSubmit={handleResetPassword} className="p-6 space-y-4">
                            {submitError && (
                                <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                                    {submitError}
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">New Password</label>
                                <input
                                    type="password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    required
                                    minLength={6}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                                    placeholder="Enter new password (min 6 characters)"
                                />
                            </div>

                            <div className="flex justify-end gap-3 pt-4">
                                <button
                                    type="button"
                                    onClick={handleClose}
                                    className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                                >
                                    {isSubmitting && (
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                    )}
                                    Reset Password
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};
