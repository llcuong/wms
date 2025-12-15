import type { ComponentType as ReactComponentType } from "react";

export type ComponentType<P = {}> = ReactComponentType<P>;

export type AppIdType = number;

export type PageIdType = string;

export interface AppNavigatorProps {
    currentApp: AppIdType;
    navigateApp: (appId: AppIdType) => void;
}

export type AppNavigatorComponent = ComponentType<AppNavigatorProps>;

export interface PageNavigatorProps extends AppNavigatorProps {
    navigatePage: (page?: PageIdType) => void;
}

export type PageNavigatorComponent = ComponentType<PageNavigatorProps>;

export type PageNavigationMap = Record<PageIdType, PageNavigatorComponent>;

export interface HistoryStateType {
    replace?: boolean;
}

export interface AppNavigationType {
    currentApp: AppIdType;
    navigateApp: (appId: AppIdType) => void;
}

export interface PageNavigationContext {
    Current: PageNavigatorComponent;
    propsApp: PageNavigatorProps;
}

export interface PageNavigationType {
    (
        currentApp: AppIdType,
        navigateApp: (appId: AppIdType) => void,
        NAVIGATE: PageNavigationMap,
        defaultPage: PageNavigatorComponent
    ): PageNavigationContext;
}

export interface HistoryState {
    app?: AppIdType;
    pages?: Record<AppIdType, PageIdType>;
}