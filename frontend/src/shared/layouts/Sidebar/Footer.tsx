import { useTranslation } from "react-i18next";

import type { Props } from "./types"

import { LogoutIcon } from "@icons";
import { useAuthStore } from "@modules/Authentication/useAuthStore";

export function Footer({ isSideBarOpen }: Props) {
    const { t } = useTranslation();

    const user = useAuthStore((state) => state.user);
    const logout = useAuthStore((state) => state.logout);

    if (!user) return null;

    return (
        <>
            <div className="w-full flex justify-center">
                <div className="w-10 h-0.5 bg-gray-200 rounded" />
            </div>
            <div className="h-10 w-full flex flex-col justify-center">
                <button type="button"
                    onClick={logout}
                    className="w-full h-10 rounded-lg flex items-center text-(--text-primary)  cursor-pointer
                                transition-colors duration-300 hover:text-(--color-primary)"
                >
                    <div className="ml-3.5">
                        <LogoutIcon />
                    </div>

                    {isSideBarOpen && (
                        <span className="font-medium overflow-hidden whitespace-nowrap ml-2.5 text-base">
                            {t("button.logout")}
                        </span>
                    )}
                </button>
            </div>
        </>
    );
};