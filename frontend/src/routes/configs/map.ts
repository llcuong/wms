import type { AppsMap } from "@routes/types";
import { APPS_CONFIG } from "./config";

export const APPS_MAP: AppsMap = APPS_CONFIG.reduce(
    (acc, app) => {
        acc[app.id] = app.navigator;
        return acc;
    },
    {} as AppsMap,
);