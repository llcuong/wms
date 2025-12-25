import { FC } from "react";

import { useAuthStore } from "@modules/Authentication/useAuthStore";

import { DropdownTheme } from "../DropdownTheme"
import { DropdownTranslation } from "../DropdownTranslation"

export const UserMenu: FC = () => {
    const user = useAuthStore((state) => state.user);

    if (!user) return null;

    return (
        <div className="flex items-center gap-3">
            <DropdownTranslation />
            <DropdownTheme />
            <div className="text-right hidden md:block">
                <p className="text-sm font-semibold text-(--text-primary)">{user.name}</p>
                <p className="text-xs text-(--text-secondary)">{user.role}</p>
            </div>

            <div className="w-10 h-10 rounded-full bg-(--color-primary) flex items-center justify-center text-(--text-primary) font-bold shadow-md">
                {user.name.charAt(0).toUpperCase()}
            </div>
        </div>
    );
};