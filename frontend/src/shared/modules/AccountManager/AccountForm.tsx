import { FC, useState } from "react";
import type { User, CreateAccountPayload } from "./types";

interface AccountFormProps {
    users: User[];
    existingAccountUserIds: string[];
    onSubmit: (payload: CreateAccountPayload) => Promise<void>;
    onCancel: () => void;
    loading?: boolean;
}

export const AccountForm: FC<AccountFormProps> = ({
    users,
    existingAccountUserIds,
    onSubmit,
    onCancel,
    loading
}) => {
    const [formData, setFormData] = useState({
        user_id: "",
        account_id: "",
        password: "",
        confirm_password: ""
    });
    const [error, setError] = useState("");

    // Lọc users chưa có account
    const availableUsers = users.filter(u => !existingAccountUserIds.includes(u.user_id));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        if (formData.password !== formData.confirm_password) {
            setError("Mật khẩu xác nhận không khớp!");
            return;
        }

        if (formData.password.length < 6) {
            setError("Mật khẩu phải có ít nhất 6 ký tự!");
            return;
        }

        await onSubmit({
            user_id: formData.user_id,
            account_id: formData.account_id,
            password: formData.password
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                    {error}
                </div>
            )}
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Người dùng <span className="text-red-500">*</span>
                </label>
                <select
                    value={formData.user_id}
                    onChange={(e) => {
                        const selectedUser = users.find(u => u.user_id === e.target.value);
                        setFormData({
                            ...formData,
                            user_id: e.target.value,
                            account_id: selectedUser?.user_name || e.target.value
                        });
                    }}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                >
                    <option value="">-- Chọn người dùng --</option>
                    {availableUsers.map((u) => (
                        <option key={u.user_id} value={u.user_id}>
                            {u.user_id} - {u.user_full_name}
                        </option>
                    ))}
                </select>
                {availableUsers.length === 0 && (
                    <p className="text-sm text-orange-600 mt-1">
                        Tất cả người dùng đã có tài khoản
                    </p>
                )}
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tên tài khoản <span className="text-red-500">*</span>
                </label>
                <input
                    type="text"
                    value={formData.account_id}
                    onChange={(e) => setFormData({ ...formData, account_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Mật khẩu <span className="text-red-500">*</span>
                </label>
                <input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                    minLength={6}
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Xác nhận mật khẩu <span className="text-red-500">*</span>
                </label>
                <input
                    type="password"
                    value={formData.confirm_password}
                    onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
            </div>
            <div className="flex justify-end gap-3 pt-4">
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                    Hủy
                </button>
                <button
                    type="submit"
                    disabled={loading || availableUsers.length === 0}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                    {loading ? "Đang tạo..." : "Tạo tài khoản"}
                </button>
            </div>
        </form>
    );
};
