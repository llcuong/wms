export const onPopState = (handler: (event: PopStateEvent) => void): (() => void) => {
    if (typeof window === "undefined") {
        return () => {};
    }
    window.addEventListener("popstate", handler);
    return () => window.removeEventListener("popstate", handler);
};