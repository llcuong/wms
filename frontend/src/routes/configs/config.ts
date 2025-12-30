import type { AppsConfig } from "@routes/types";

import { PackingIcon, FormerIcon, FinishedIcon, SemiFinishedIcon, AccountIcon, DataIcon } from "@icons"
import { Navigate as SemiFinishedNavigate } from "../../apps/public/semi-finished/Navigate"
import { Navigate as FinishedNavigate } from "../../apps/public/finished/Navigate"
import { Navigate as FormerNavigate } from "../../apps/public/former/Navigate"
import { Navigate as PackingNavigate } from "../../apps/public/packing/Navigate"
import { Navigate as ManageAccountNavigate } from "@manage-account/Navigate"
import { Navigate as ManageDataNavigate } from "@manage-data/Navigate"

export const PUBLIC_CONFIGS: AppsConfig[] = [
    {
        id: 1,
        name: "Packing",
        icon: PackingIcon,
        navigator: PackingNavigate,
    },
    {
        id: 2,
        name: "Former",
        icon: FormerIcon,
        navigator: FormerNavigate,
    },
    {
        id: 3,
        name: "Semi-finished",
        icon: SemiFinishedIcon,
        navigator: SemiFinishedNavigate,
    },
    {
        id: 4,
        name: "Finished",
        icon: FinishedIcon,
        navigator: FinishedNavigate,
    }
];

export const SETTING_CONFIGS: AppsConfig[] = [

];

export const ADMIN_CONFIGS: AppsConfig[] = [
    {
        id: 10,
        name: "Data models",
        icon: DataIcon,
        navigator: ManageDataNavigate,
    },
    {
        id: 11,
        name: "Accounts",
        icon: AccountIcon,
        navigator: ManageAccountNavigate,
    }
];

export const APPS_CONFIG: AppsConfig[] = [...PUBLIC_CONFIGS, ...SETTING_CONFIGS, ...ADMIN_CONFIGS];