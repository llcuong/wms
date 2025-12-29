import { Tree } from "react-arborist";

import { TreeNodeModel, TreeNodeType } from "./tree.types";

import { TreeNode } from "./TreeNode";

interface TreeStructureProps {
    data: TreeNodeModel[];
    onAdd: (parentId: string, type: TreeNodeType) => void;
    onRename: (id: string, name: string) => void;
    onDelete: (id: string) => void;
};

export function TreeStructure({
    data,
    onAdd,
    onRename,
    onDelete,
}: TreeStructureProps) {
    return (
        <Tree<TreeNodeModel>
            data={data}
            childrenAccessor="children"
            openByDefault
            width="100%"
            height={500}
        >
            {(props) => (
                <TreeNode
                    {...props}
                    onAdd={onAdd}
                    onRename={onRename}
                    onDelete={onDelete}
                />
            )}
        </Tree>
    );
};