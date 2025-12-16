import { useEffect, useState } from "react";

const SIDEBAR_KEY = "__sidebar_state__";

export function useSidebarState(defaultValue = false) {
    const [isSideBarOpen, setSideBarOpen] = useState<boolean>(() => {
        if (typeof window === "undefined") return defaultValue;

        try {
            return localStorage.getItem(SIDEBAR_KEY) === "true";
        } catch {
            return defaultValue;
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem(SIDEBAR_KEY, String(isSideBarOpen));
        } catch {
            // ignore
        }
    }, [isSideBarOpen]);

    return {
        isSideBarOpen,
        setSideBarOpen,
        toggleSideBar: () => setSideBarOpen(v => !v),
    };
}
