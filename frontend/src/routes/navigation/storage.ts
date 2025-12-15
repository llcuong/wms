import { DEFAULT_APP, DEFAULT_PAGE, CURRENT_APP_KEY, CURRENT_PAGE_KEY, APPS_CONFIG } from "@routes/configs";
import type { AppIdType, PageIdType } from "@routes/types";
import { createIsValidApp, isBrowser, safeParseJSON } from "@routes/utils";

export const isValidApp = (candidate: unknown): boolean => {
    const validator = createIsValidApp(APPS_CONFIG.map(app => app.id));
    return validator(candidate as number | string | null | undefined);
};

export const getAppFn = (): AppIdType => {
    if (!isBrowser) return DEFAULT_APP;

    try {
        const appFromHistory = history.state?.app as AppIdType | undefined;
        const appFromLocalRaw = localStorage.getItem(CURRENT_APP_KEY);

        let candidate: AppIdType;

        if (appFromHistory !== undefined) {
            candidate = appFromHistory;
        } else if (appFromLocalRaw) {
            candidate = Number(appFromLocalRaw);
        } else {
            candidate = DEFAULT_APP;
        }

        return isValidApp(candidate) ? candidate : DEFAULT_APP;
    } catch {
        return DEFAULT_APP;
    }
};

export const getPageFn = (appId: AppIdType, defaultPage: PageIdType = DEFAULT_PAGE): PageIdType => {
    if (!isBrowser) return defaultPage;

    try {
        const state = history.state as { pages?: Record<string, PageIdType> } | null;
        const fromHistory = state?.pages?.[appId];

        const map = safeParseJSON<Record<string, PageIdType>>(
            localStorage.getItem(CURRENT_PAGE_KEY),
            {},
        );
        const fromLocal = map[appId];

        return (fromHistory || fromLocal || defaultPage) as PageIdType;
    } catch {
        return defaultPage;
    }
};

export const saveAppFn = (appId: AppIdType): void => {
    if (!isBrowser) return;
    try {
        localStorage.setItem(CURRENT_APP_KEY, String(appId));
    } catch {
        // ignore
    }
};

export const savePageFn = (appId: AppIdType, pageId: PageIdType): void => {
    if (!isBrowser) return;

    try {
        const map = safeParseJSON<Record<string, PageIdType>>(
            localStorage.getItem(CURRENT_PAGE_KEY),
            {},
        );
        map[appId] = pageId;
        localStorage.setItem(CURRENT_PAGE_KEY, JSON.stringify(map));
    } catch {
        // ignore
    }
};