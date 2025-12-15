import type { AppsConfig } from "@routes/types";

import HomeIcon from "@icons/HomeIcon"
import {Navigate as SemiFinishedNavigate} from "@semi-finished/Navigate"
import {Navigate as FinishedNavigate} from "@finished/Navigate"

export const APPS_CONFIG: AppsConfig[] = [
    {
        id: 1,
        name: "Semi-finished",
        icon: HomeIcon,
        navigator: SemiFinishedNavigate,
    },
    {
        id: 2,
        name: "Finished",
        icon: HomeIcon,
        navigator: FinishedNavigate,
    }
];