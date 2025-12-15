import type { AppsConfig } from "@routes/types";

import FormerIcon from "@icons/FormerIcon"
import FinishedIcon from "@icons/FinishedIcon"
import SemiFinishedIcon from "@icons/SemiFinishedIcon"
import {Navigate as SemiFinishedNavigate} from "@semi-finished/Navigate"
import {Navigate as FinishedNavigate} from "@finished/Navigate"
import {Navigate as FormerNavigate} from "@former/Navigate"

export const APPS_CONFIG: AppsConfig[] = [
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