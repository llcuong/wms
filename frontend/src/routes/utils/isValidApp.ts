import type { AppIdType } from "@routes/types";
import { createIsInSet } from "./isInSet";

export type IsValidAppType = (app: number | string | null | undefined) => app is AppIdType;

export const createIsValidApp = (ids: readonly AppIdType[]): IsValidAppType =>
    createIsInSet<AppIdType>(ids);