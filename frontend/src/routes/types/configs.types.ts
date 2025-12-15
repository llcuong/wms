import type { SVGProps } from "react";
import type { AppIdType, AppNavigatorComponent, ComponentType } from "./navigation.types";

export interface AppsConfig {
    id: AppIdType;
    name: string;
    icon: ComponentType<SVGProps<SVGSVGElement>>;
    navigator: AppNavigatorComponent;
}

export type AppsMap = Record<AppIdType, AppNavigatorComponent>;