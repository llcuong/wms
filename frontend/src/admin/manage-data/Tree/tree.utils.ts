import { TreeNodeModel } from "./tree.types";

export function addChild(nodeList: TreeNodeModel[], newNode: TreeNodeModel): TreeNodeModel[] {
    return nodeList.map((node) => {
        if (node.id === newNode.parentId) return { ...node, children: [...(node.children ?? []), newNode] };
        if (Array.isArray(node.children) && node.children.length > 0 && Array.isArray(newNode.children) && newNode.children.length > 0) {
            return { ...newNode, children: addChild(newNode.children, newNode) };
        };
        return node;
    });
};

export function updateNode(nodeList: TreeNodeModel[], id: string, name: string): TreeNodeModel[] {
    return nodeList.map((node) => {
        if (node.id === id) return { ...node, name };
        if (node.children) return { ...node, children: updateNode(node.children, id, name) };
        return node;
    });
};

export function deleteNode(nodeList: TreeNodeModel[], id: string): TreeNodeModel[] {
    return nodeList.filter((node) => node.id !== id)
        .map((node) => node.children ? { ...node, children: deleteNode(node.children, id) } : node);
};