import { BranchIcon, FactoryIcon, LineIcon, MachineIcon } from "@icons";
import { FC, SVGProps } from "react";

export type TreeNodeType = "factory" | "branch" | "machine" | "line";

export interface TreeNodeModel {
    id: string;
    parentId?: string;
    name: string;
    code: string;
    type: TreeNodeType;
    icon?: FC<SVGProps<SVGSVGElement>>;
    children?: TreeNodeModel[];
};

export const TREE_TYPE_ICONS: Record<TreeNodeType, FC<SVGProps<SVGSVGElement>>> = {
    factory: FactoryIcon,
    branch: BranchIcon,
    machine: MachineIcon,
    line: LineIcon,
};