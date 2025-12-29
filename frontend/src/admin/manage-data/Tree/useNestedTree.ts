import { useState } from "react";

import { TreeNodeModel, TreeNodeType } from "./tree.types";

import { addChild, updateNode, deleteNode } from "./tree.utils";

export default function useNestedTree(initialData: TreeNodeModel[]) {
    const [data, setData] = useState<TreeNodeModel[]>(initialData);

    function createChild(parentId: string, type: TreeNodeType) {
        setData((prev) => addChild(prev, {
            id: "test",
            parentId: parentId,
            name: "New node",
            code: "newNode",
            type: type,
        }));
    };

    function renameNode(id: string, name: string) {
        setData((prev) => updateNode(prev, id, name));
    };

    function removeNode(id: string) {
        setData((prev) => deleteNode(prev, id));
    };

    return {
        data,
        createChild,
        renameNode,
        removeNode,
    };
};