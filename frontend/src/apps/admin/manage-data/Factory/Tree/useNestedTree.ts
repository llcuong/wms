import { useEffect, useState } from "react";

import { TreeHooks, TreeNodeModel } from "./tree.types";

import { updateNode, deleteNode, addNode } from "./tree.utils";

export default function useNestedTree(
    initialData: TreeNodeModel[],
    hooks?: TreeHooks<TreeNodeModel>
) {
    const [data, setData] = useState<TreeNodeModel[]>(initialData);

    useEffect(() => {
        setData(initialData);
    }, [initialData]);

    function createNode(newNode: TreeNodeModel) {
        setData((prev) => addNode(prev, newNode, hooks));
    };

    function updateNoteById(id: string, updater: (node: TreeNodeModel) => TreeNodeModel, parentId?: string) {
        setData((prev) => updateNode(prev, id, updater, hooks, parentId));
    };

    function deleteNodeById(id: string, parentId?: string) {
        setData((prev) => deleteNode(prev, id, hooks, parentId));
    };

    return {
        data,
        createNode,
        updateNoteById,
        deleteNodeById,
    };
};