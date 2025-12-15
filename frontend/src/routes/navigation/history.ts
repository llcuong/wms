import type { AppIdType, PageIdType, HistoryStateType, HistoryState } from "@routes/types";
import { isBrowser } from "@routes/utils";

export const setAppFn = (appId: AppIdType, { replace = false }: HistoryStateType = {}): void => {
    if (!isBrowser) return;
    try {
        const prev = (history.state as HistoryState | null) || {};
        const next: HistoryState = { ...prev, app: appId };
        const method: "pushState" | "replaceState" = replace ? "replaceState" : "pushState";
        history[method](next, "", "/");
    } catch {
    }
};

export const setPageFn = (appId: AppIdType, pageId: PageIdType): void => {
    if (!isBrowser) return;
    try {
        const prev = (history.state as HistoryState | null) || {};
        const pages = {
            ...(prev.pages || {}),
            [appId]: pageId,
        };
        const next: HistoryState = {
            app: prev.app ?? appId,
            pages,
        };
        history.replaceState(next, "", "/");
    } catch {
    }
};