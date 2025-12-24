import { THEME } from "@routes/configs";
import { useCallback, useEffect, useState } from "react";

const DEFAULT_THEME: Theme = "light";

const THEMES = ["light", "dark", "mars", "laserwave"] as const;

export type Theme = (typeof THEMES)[number];

export default function useTheme() {
    const [themeState, setThemeState] = useState<Theme>(() => {
        if (typeof window === "undefined") return DEFAULT_THEME;

        const stored = localStorage.getItem(THEME) as Theme | null;
        return stored && THEMES.includes(stored) ? stored : DEFAULT_THEME;
    });

    const setTheme = useCallback((nextTheme: Theme) => {
        setThemeState(nextTheme);
        localStorage.setItem(THEME, nextTheme);
    }, []);

    useEffect(() => {
        document.documentElement.setAttribute("data-theme", themeState);
    }, [themeState]);

    return { themeState, setTheme, themes: THEMES };
};