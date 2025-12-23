import type { AppsConfig } from "@routes/types";

import { FormerIcon, FinishedIcon, SemiFinishedIcon, AccountIcon, DataIcon } from "@icons"
import { Navigate as SemiFinishedNavigate } from "@semi-finished/Navigate"
import { Navigate as FinishedNavigate } from "@finished/Navigate"
import { Navigate as FormerNavigate } from "@former/Navigate"
import { Navigate as ManageAccountNavigate } from "@manage-account/Navigate"

export const PUBLIC_CONFIGS: AppsConfig[] = [
    {
        id: 1,
        name: "Former",
        icon: FormerIcon,
        navigator: FormerNavigate,
    },
    {
        id: 2,
        name: "Semi-finished",
        icon: SemiFinishedIcon,
        navigator: SemiFinishedNavigate,
    },
    {
        id: 3,
        name: "Finished",
        icon: FinishedIcon,
        navigator: FinishedNavigate,
    }
];

export const PRIVATE_CONFIGS: AppsConfig[] = [
    {
        id: 4,
        name: "Data models",
        icon: DataIcon,
        navigator: ManageAccountNavigate,
    },
    {
        id: 5,
        name: "Accounts",
        icon: AccountIcon,
        navigator: ManageAccountNavigate,
    }
];

export const APPS_CONFIG: AppsConfig[] = [...PUBLIC_CONFIGS, ...PRIVATE_CONFIGS];