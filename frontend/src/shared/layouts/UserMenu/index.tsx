import { FC } from "react";
import { useAuthStore } from "@modules/Login/useAuthStore";

export const UserMenu: FC = () => {
    const user = useAuthStore((state) => state.user);

    if (!user) return null;

    return (
        <div className="flex items-center gap-3">
            <div className="text-right hidden md:block">
                <p className="text-sm font-semibold text-gray-800">{user.name}</p>
                <p className="text-xs text-gray-500">{user.role}</p>
            </div>

            <div className="w-10 h-10 rounded-full bg-linear-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold shadow-md">
                {user.name.charAt(0).toUpperCase()}
            </div>
        </div>
    );
};
