import type { AppIdType } from "@routes/types";
import { createIsInSet } from "./isInSet";

export type IsHasAppType = (id: number | string | null | undefined) => id is AppIdType;

export const createIsHasApp = (ids: readonly AppIdType[]): IsHasAppType =>
    ((value: number | string | null | undefined): value is AppIdType =>
        createIsInSet<AppIdType>(ids)(value)) as IsHasAppType;