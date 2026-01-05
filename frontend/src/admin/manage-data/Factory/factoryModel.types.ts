export interface FactoryModel {
    factory_code: string;
    factory_name: string;
};

export interface BranchModel {
    id: number;
    factory_code: string;
    branch_type: string;
    branch_code: string;
    branch_name: string;
};

export interface MachineModel {
    id: number;
    branch_code: string;
    machine_code: string;
    machine_name: string;
};

export interface MachineLineModel {
    id: number;
    machine_code: string;
    line_code: string;
    line_name: string;
};

export type TreeNodeType = "root" | "factory" | "branch" | "machine" | "line";

interface TreeNodeBase {
    type: TreeNodeType;
}

export interface MachineLineNode extends TreeNodeBase, MachineLineModel {
    type: "line";
    children?: never;
};

export interface MachineNode extends TreeNodeBase, MachineModel {
    type: "machine";
    children?: MachineLineNode[];
};

export interface BranchNode extends TreeNodeBase, BranchModel {
    type: "branch";
    children?: MachineNode[];
};

export interface FactoryNode extends TreeNodeBase, FactoryModel {
    type: "factory";
    children?: BranchNode[];
};

type FactoryMeta = {
    code: string;
    parentCode?: string;
};

export type MetaMap = Record<string, FactoryMeta>;