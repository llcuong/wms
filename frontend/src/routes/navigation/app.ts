import { useState, useEffect, useCallback } from "react";
import type { AppIdType, AppNavigationType, HistoryState } from "@routes/types";
import { getAppFn, saveAppFn } from "./storage";
import { setAppFn } from "./history";
import { onPopState } from "./state";
import { createIsHasApp } from "@routes/utils";
import { APPS_MAP } from "@routes/configs";

const APP_ID_LIST = Object.keys(APPS_MAP).map(Number) as AppIdType[];
const isHasAppBase = createIsHasApp(APP_ID_LIST);
const isHasApp = (id: any): id is AppIdType => isHasAppBase(id);

export const useAppNavigation = (): AppNavigationType => {
    const [currentApp, setCurrentApp] = useState<AppIdType>(() => getAppFn());

    const navigateApp = useCallback((next: AppIdType) => {
        setCurrentApp((prev) => {
            if (next === prev) return prev;
            if (!isHasApp(next)) return prev;

            setAppFn(next);
            return next;
        });
    }, []);

    useEffect(() => {
        if (typeof window === "undefined") return;

        const state = history.state as HistoryState | null;
        if (!state?.app || !isHasApp(state.app)) {
            setAppFn(currentApp, { replace: true });
        }

        const unbind = onPopState((e: PopStateEvent) => {
            const next = (e.state as HistoryState | null)?.app;
            if (isHasApp(next)) {
                setCurrentApp(next);
            } else {
                setCurrentApp(getAppFn());
            }
        });

        return unbind;
    }, []);

    useEffect(() => {
        saveAppFn(currentApp);
    }, [currentApp]);

    return { currentApp, navigateApp };
};