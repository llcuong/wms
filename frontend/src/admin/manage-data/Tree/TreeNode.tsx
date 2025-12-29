import { NodeRendererProps } from "react-arborist";

import { TREE_TYPE_ICONS, TreeNodeModel, TreeNodeType } from "./tree.types";

interface TreeNodeProps extends NodeRendererProps<TreeNodeModel> {
    onAdd: (parentId: string, type: TreeNodeType) => void;
    onRename: (id: string, name: string) => void;
    onDelete: (id: string) => void;
}

export function TreeNode({
    node,
    style,
    onAdd,
    onRename,
    onDelete,
}: TreeNodeProps) {
    const { id, name, type, icon } = node.data;
    const Icon = icon ?? TREE_TYPE_ICONS[type];

    return (
        <div
            style={style}
            className="flex items-center justify-between hover:bg-gray-100 cursor-grab"
        >
            <div className="flex items-center gap-2">
                <Icon className="w-4 h-4 text-indigo-600" />
                <span className="font-medium">{name}</span>
            </div>

            <div className="flex gap-2">
                <button
                    onClick={() => onAdd(id, type)}
                    className="text-xs text-indigo-600"
                >
                    + Child
                </button>

                <button
                    onClick={() => {
                        const v = prompt("Rename", name);
                        if (v) onRename(id, v);
                    }}
                    className="text-xs text-gray-600"
                >
                    Edit
                </button>

                <button
                    onClick={() => onDelete(id)}
                    className="text-xs text-red-600"
                >
                    Delete
                </button>
            </div>
        </div>
    );
};