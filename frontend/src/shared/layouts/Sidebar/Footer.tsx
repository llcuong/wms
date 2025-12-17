import { FC } from "react";
import { useAuthStore } from "@modules/Login/useAuthStore";
import type { Props } from "./types"

export function Footer({ isSideBarOpen, toggleSidebar }: Props) {
    const user = useAuthStore((state) => state.user);
    const logout = useAuthStore((state) => state.logout);

    if (!user) return null;

    return (
        <>
            <div className="w-full flex justify-center">
                <div className="w-10 h-0.5 bg-gray-200 rounded" />
            </div>
            <div className="h-10 w-full flex flex-col justify-center cursor-pointer">
                <button
                    onClick={logout}
                    className={`w-full h-10 rounded-lg flex items-center transition-colors "text-(--text-primary) hover:text-(--color-primary)`}
                >
                    <div className="ml-3.5">
                       <svg className="w-6.5 h-6.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                    </div>

                    {isSideBarOpen && (
                        <span className="font-medium overflow-hidden whitespace-nowrap ml-2.5 text-base">
                            Logout
                        </span>
                    )}
                </button>
            </div>
        </>
    );
}