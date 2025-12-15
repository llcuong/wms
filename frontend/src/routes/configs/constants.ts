import { APPS_CONFIG } from "./config";

export const DEFAULT_APP = 1 as const;

export const DEFAULT_PAGE = "index" as const;
export const CURRENT_APP_KEY = "__current_app__";
export const CURRENT_PAGE_KEY = "__current_page__";

export const APP_IDS: number[] = APPS_CONFIG.map(app => app.id);