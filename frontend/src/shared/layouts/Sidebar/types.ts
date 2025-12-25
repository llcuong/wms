import type { PageNavigatorProps } from "@routes/types";

export interface SidebarProps extends PageNavigatorProps {
    isSideBarOpen: boolean;
    setSideBarOpen: (value: boolean | ((prev: boolean) => boolean)) => void;
}

export interface Props {
    isSideBarOpen: boolean;
    toggleSidebar?: () => void;
}