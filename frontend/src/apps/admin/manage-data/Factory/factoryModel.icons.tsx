import { TreeIconRender } from "./Tree/tree.types";

import { BranchIcon, FactoryIcon, FolderIcon, LineIcon, MachineIcon } from "@icons";

export const factoryTreeIconRender: TreeIconRender = (node) => {
    switch (node.type) {
        case "factory":
            return <FactoryIcon className="w-4 h-4 text-indigo-600" />;
        case "branch":
            return <BranchIcon className="w-4 h-4 text-indigo-600" />;
        case "machine":
            return <MachineIcon className="w-4 h-4 text-indigo-600" />;
        case "line":
            return <LineIcon className="w-4 h-4 text-indigo-600" />;
        default:
            return <FolderIcon className="w-4 h-4 text-indigo-600" />;
    }
};