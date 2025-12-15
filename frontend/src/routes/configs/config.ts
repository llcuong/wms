import type { AppsConfig } from "@routes/types";

import HomeIcon from "@icons/HomeIcon"
import {Navigate as SemiFinishedNavigate} from "@semi-finished/Navigate"
import {Navigate as FinishedNavigate} from "@finished/Navigate"
import {Navigate as FormerNavigate} from "@former/Navigate"

export const APPS_CONFIG: AppsConfig[] = [
    {
        id: 1,
        name: "Former",
        icon: HomeIcon,
        navigator: FormerNavigate,
    },
    {
        id: 2,
        name: "Semi-finished",
        icon: HomeIcon,
        navigator: SemiFinishedNavigate,
    },
    {
        id: 3,
        name: "Finished",
        icon: HomeIcon,
        navigator: FinishedNavigate,
    }
];