import React from "react";
import { Tree } from "react-arborist";

import { TreeIconRender, TreeNodeModel } from "./tree.types";

import { TreeNode } from "./TreeNode";

export interface TreeStructureProps {
    data: TreeNodeModel[];
    onAdd: (parent: TreeNodeModel) => void;
    onUpdate: (node: TreeNodeModel, prev: TreeNodeModel) => void;
    onDelete: (node: TreeNodeModel) => void;
    renderIcon: TreeIconRender;
    popupContent: React.ReactNode;
};

export function TreeStructure({
    data,
    renderIcon,
    popupContent,
    onAdd,
    onUpdate,
    onDelete,
}: TreeStructureProps) {
    return (
        <Tree<TreeNodeModel>
            data={data}
            childrenAccessor="children"
            openByDefault
            width="100%"
            height={750}
            rowHeight={30}
        >
            {(props) => (
                <TreeNode
                    {...props}
                    onAdd={onAdd}
                    onUpdate={onUpdate}
                    onDelete={onDelete}
                    renderIcon={renderIcon}
                    popupContent={popupContent}
                />
            )}
        </Tree>
    );
};