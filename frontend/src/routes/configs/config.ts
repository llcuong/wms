import type { AppsConfig } from "@routes/types";

import { FormerIcon, FinishedIcon, SemiFinishedIcon, ManageIcon } from "@icons"
import { Navigate as SemiFinishedNavigate } from "@semi-finished/Navigate"
import { Navigate as FinishedNavigate } from "@finished/Navigate"
import { Navigate as FormerNavigate } from "@former/Navigate"

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
        name: "Manage",
        icon: ManageIcon,
        navigator: FormerNavigate,
    }
];

export const APPS_CONFIG: AppsConfig[] = [...PUBLIC_CONFIGS, ...PRIVATE_CONFIGS];