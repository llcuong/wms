import { TreeHooks, TreeNodeModel } from "./tree.types";

export function addNode(
    nodeList: TreeNodeModel[],
    newNode: TreeNodeModel,
    hooks?: TreeHooks<TreeNodeModel>
): TreeNodeModel[] {
    return nodeList.map((node) => {
        if (node.id === newNode.parentId) {
            hooks?.onAdd?.(newNode, node);
            return { ...node, children: [...(node.children ?? []), newNode] };
        };
        if (node.children) return { ...node, children: addNode(node.children, newNode, hooks) };
        return node;
    })
};

export function updateNode(
    nodeList: TreeNodeModel[],
    id: string,
    updater: (node: TreeNodeModel) => TreeNodeModel,
    hooks?: TreeHooks<TreeNodeModel>,
    parentId?: string,
): TreeNodeModel[] {
    return nodeList.map((node) => {
        const isMatch = node.id === id && (parentId === undefined || node.parentId === parentId);
        if (isMatch) {
            const updated = updater(node);
            hooks?.onUpdate?.(updated, node);
            return { ...updated, children: node.children };
        };
        if (node.children) return {
            ...node,
            children: updateNode(node.children, id, updater, hooks, parentId)
        };
        return node;
    })
};

export function deleteNode(
    nodeList: TreeNodeModel[],
    id: string,
    hooks?: TreeHooks<TreeNodeModel>,
    parentId?: string,
): TreeNodeModel[] {
    return nodeList
        .filter((node) => {
            const isMatch = node.id === id && (parentId === undefined || node.parentId === parentId);
            if (isMatch) {
                hooks?.onDelete?.(node);
                return false;
            };
            return true;
        })
        .map((node) => node.children ? { ...node, children: deleteNode(node.children, id, hooks, parentId) } : node);
};