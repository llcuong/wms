import type { AppsConfig } from "@routes/types";

import { Navigate as FormerNavigate } from "@former/Navigate"
import { Navigate as FinishedNavigate } from "@finished/Navigate"
import { Navigate as ManageDataNavigate } from "@manage-data/Navigate"
import { Navigate as SemiFinishedNavigate } from "@semi-finished/Navigate"
import { Navigate as ManageAccountNavigate } from "@manage-account/Navigate"
import { FormerIcon, FinishedIcon, SemiFinishedIcon, AccountIcon, DataIcon } from "@icons"

export const PUBLIC_CONFIGS: AppsConfig[] = [
    {
        id: 1,
        name: "former",
        icon: FormerIcon,
        navigator: FormerNavigate,
    },
    {
        id: 2,
        name: "semiFinished",
        icon: SemiFinishedIcon,
        navigator: SemiFinishedNavigate,
    },
    {
        id: 3,
        name: "finished",
        icon: FinishedIcon,
        navigator: FinishedNavigate,
    }
];

export const PRIVATE_CONFIGS: AppsConfig[] = [
    {
        id: 4,
        name: "dataModels",
        icon: DataIcon,
        navigator: ManageDataNavigate,
    },
    {
        id: 5,
        name: "accounts",
        icon: AccountIcon,
        navigator: ManageAccountNavigate,
    }
];

export const APPS_CONFIG: AppsConfig[] = [...PUBLIC_CONFIGS, ...PRIVATE_CONFIGS];