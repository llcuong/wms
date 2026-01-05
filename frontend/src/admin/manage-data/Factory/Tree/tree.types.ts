import { ReactNode } from "react";

export interface TreeNodeModel {
    id: string;
    parentId?: string;
    name: string;
    type: string;
    children?: TreeNodeModel[];
    isFirst?: boolean;
    isLast?: boolean;
};

export type TreeIconRender = (node: TreeNodeModel) => ReactNode;

export interface TreeHooks<T> {
    onAdd: (node: T, parent?: T) => void;
    onUpdate: (node: T, prev: T) => void;
    onDelete: (node: T) => void;
};

export type OpenType = "create" | "update" | "delete";