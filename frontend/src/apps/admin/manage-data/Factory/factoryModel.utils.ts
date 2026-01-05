import { TreeNodeModel } from "./Tree/tree.types";
import { BranchNode, FactoryNode, MachineLineNode, MachineNode, MetaMap } from "./factoryModel.types";

const DUMMY_ROOT_ID = "__root__";
const DUMMY_ROOT_TYPE = "root";

export function createDummyRoot(children: TreeNodeModel[]): TreeNodeModel[] {
    return [{
        id: DUMMY_ROOT_ID,
        name: "Main",
        type: DUMMY_ROOT_TYPE,
        isFirst: true,
        children,
    }];
};

export function factoryTreeToGeneric(
    factoryList: FactoryNode[]
): { tree: TreeNodeModel[]; meta: MetaMap } {
    const meta: MetaMap = {};

    function mapLine(line: MachineLineNode, parent: MachineNode): TreeNodeModel {
        meta[line.id] = {
            code: line.line_code,
            parentCode: parent.machine_code,
        };

        return {
            id: line.line_code,
            parentId: parent.machine_code,
            name: line.line_name,
            type: "line",
            isLast: true,
        };
    };

    function mapMachine(machine: MachineNode, parent: BranchNode): TreeNodeModel {
        meta[machine.id] = {
            code: machine.machine_code,
            parentCode: parent.branch_code,
        };

        return {
            id: machine.machine_code,
            parentId: parent.branch_code,
            name: machine.machine_name,
            type: "machine",
            children: machine.children?.map((line) => mapLine(line, machine))
        };
    };

    function mapBranch(branch: BranchNode, parent: FactoryNode): TreeNodeModel {
        meta[branch.id] = {
            code: branch.branch_code,
            parentCode: parent.factory_code,
        };

        return {
            id: branch.branch_code,
            parentId: parent.factory_code,
            name: branch.branch_name,
            type: "branch",
            children: branch.children?.map((machine) => mapMachine(machine, branch))
        }
    };

    const tree = factoryList.map((factory) => {
        meta[factory.factory_code] = {
            code: factory.factory_code,
            parentCode: "root",
        };

        return {
            id: factory.factory_code,
            parentId: DUMMY_ROOT_ID,
            name: factory.factory_name,
            type: "factory",
            children: factory.children?.map((branch) => mapBranch(branch, factory)),
        };
    });

    return { tree, meta };
};