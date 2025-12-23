import { FC, useState } from "react";
import type { User, UserStatus, CreateUserPayload, UpdateUserPayload } from "./types";

interface UserFormProps {
    user?: User | null;
    statuses: UserStatus[];
    onSubmit: (payload: CreateUserPayload | UpdateUserPayload) => Promise<void>;
    onCancel: () => void;
    loading?: boolean;
}

export const UserForm: FC<UserFormProps> = ({ user, statuses, onSubmit, onCancel, loading }) => {
    const [formData, setFormData] = useState({
        user_id: user?.user_id || "",
        user_name: user?.user_name || "",
        user_full_name: user?.user_full_name || "",
        user_email: user?.user_email || "",
        user_status_id: user?.user_status?.status_id?.toString() || statuses[0]?.status_id?.toString() || ""
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await onSubmit({
            ...formData,
            user_status_id: parseInt(formData.user_status_id)
        });
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Mã nhân viên <span className="text-red-500">*</span>
                </label>
                <input
                    type="text"
                    value={formData.user_id}
                    onChange={(e) => setFormData({ ...formData, user_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none disabled:bg-gray-100"
                    required
                    disabled={!!user}
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tên đăng nhập <span className="text-red-500">*</span>
                </label>
                <input
                    type="text"
                    value={formData.user_name}
                    onChange={(e) => setFormData({ ...formData, user_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Họ và tên <span className="text-red-500">*</span>
                </label>
                <input
                    type="text"
                    value={formData.user_full_name}
                    onChange={(e) => setFormData({ ...formData, user_full_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                    type="email"
                    value={formData.user_email}
                    onChange={(e) => setFormData({ ...formData, user_email: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                />
            </div>
            <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                    Trạng thái <span className="text-red-500">*</span>
                </label>
                <select
                    value={formData.user_status_id}
                    onChange={(e) => setFormData({ ...formData, user_status_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    required
                >
                    <option value="">-- Chọn --</option>
                    {statuses.map((s) => (
                        <option key={s.status_id} value={s.status_id}>{s.status_name}</option>
                    ))}
                </select>
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
                    disabled={loading}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                    {loading ? "Đang lưu..." : "Lưu"}
                </button>
            </div>
        </form>
    );
};
