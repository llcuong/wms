import type { FC, ReactNode } from "react";
import type { PageNavigatorProps } from "@routes/types";

export interface AppsBaseProps extends PageNavigatorProps {
    navbarTitle?: ReactNode;
    mainContent?: ReactNode;
}

export type AppsBaseComponent = FC<AppsBaseProps>;