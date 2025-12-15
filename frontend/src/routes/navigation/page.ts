import { useState, useEffect, useMemo, useCallback } from "react";
import type { PageNavigatorProps, PageIdType, PageNavigationType, HistoryState } from "@routes/types";
import { getPageFn, savePageFn } from "./storage";
import { setPageFn } from "./history";
import { onPopState } from "./state";

export const usePageNavigation: PageNavigationType = (currentApp, navigateApp, NAVIGATE, defaultPage) => {
    const [page, setPage] = useState<PageIdType>(() => getPageFn(currentApp, "index"));
    useEffect(() => {
        setPage(getPageFn(currentApp, "index"));
    }, [currentApp]);

    const navigatePage = useCallback((next: PageIdType = "index") => {
        setPage((prev) => {
            if (next === prev) return prev;
            savePageFn(currentApp, next);
            setPageFn(currentApp, next);
            return next;
        });
    }, [currentApp]);

    const propsApp: PageNavigatorProps = useMemo(() => ({
        currentApp,
        navigateApp,
        navigatePage
    }), [currentApp, navigateApp, navigatePage]);

    useEffect(() => {
        const state = history.state as HistoryState | null;
        if (!state?.pages?.[currentApp]) {
            setPageFn(currentApp, page);
        }

        const unbind = onPopState((e: PopStateEvent) => {
            const next = (e.state as HistoryState | null)?.pages?.[currentApp];
            if (next) setPage(next);
        });

        return unbind;
    }, [currentApp]);

    const Current = NAVIGATE[page] ?? defaultPage;

    return { Current, propsApp };
};