import type { PageNavigatorProps, ExtraAppConfig } from "@routes/types";

export interface SidebarProps extends PageNavigatorProps {
    isSideBarOpen: boolean;
    setSideBarOpen: (value: boolean | ((prev: boolean) => boolean)) => void;
    extraPrivateApps?: ExtraAppConfig[];
}
