import React, { useState } from "react";
import { NodeRendererProps } from "react-arborist";

import { OpenType, TreeHooks, TreeIconRender, TreeNodeModel } from "./tree.types";
import { TreeNodeType } from "../factoryModel.types";

import { Popup } from "@layouts";
import { DeleteIcon, EditIcon, PlusIcon } from "@icons";

interface ButtonData {
    key: OpenType | "cancel" | "unknown";
    type: React.ButtonHTMLAttributes<HTMLButtonElement>["type"];
    onClick: (() => void) | undefined;
    className: string;
    label: string;
};

interface PopupData {
    key: OpenType;
    title: string;
    description: string;
    content?: React.ReactNode;
};

interface PopupSectionProps {
    isOpen: boolean;
    openType: OpenType;
    handleClosePopup: () => void;
    content: React.ReactNode;
    buttonAction: TreeHooks<TreeNodeModel>;
    node: NodeRendererProps<TreeNodeModel>["node"];
};

const PopupSection = ({
    isOpen,
    openType,
    handleClosePopup,
    content,
    node,
    buttonAction,
}: PopupSectionProps) => {
    const getPopupData = () => {
        let popupData: PopupData | undefined;
        switch (openType) {
            case "create":
                popupData = {
                    key: "create",
                    title: "title.create{{node}}",
                    description: "description.create{{node}}",
                    content: content,
                };
                break;
            case "update":
                popupData = {
                    key: "update",
                    title: "title.update{{node}}",
                    description: "description.update{{node}}",
                    content: content,
                };
                break;
            case "delete":
                popupData = {
                    key: "delete",
                    title: "title.delete{{node}}",
                    description: "description.delete{{node}}",
                    content: content,
                };
                break;
            default:
                popupData = undefined;
                break;
        };
        return popupData;
    };

    const getPopupButton = () => {
        let buttonData: ButtonData | undefined;
        switch (openType) {
            case "create":
                buttonData = {
                    key: "create",
                    type: "button",
                    onClick: () => buttonAction.onAdd(node.data),
                    className: "bg-green-600 text-white",
                    label: "Create",
                };
                break;
            case "update":
                buttonData = {
                    key: "update",
                    type: "button",
                    onClick: () => {
                        const v = prompt("Rename", node.data.name);
                        if (v) {
                            buttonAction.onUpdate(
                                { ...node.data, name: v },
                                node.data
                            );
                        }
                    },
                    className: "bg-green-600 text-white",
                    label: "Save",
                };
                break;
            case "delete":
                buttonData = {
                    key: "create",
                    type: "button",
                    onClick: () => buttonAction.onDelete(node.data),
                    className: "bg-red-600 text-white",
                    label: "Delete"
                };
                break;
            default:
                buttonData = undefined;
                break;
        };
        return buttonData;
    };

    const BUTTON_LIST: ButtonData[] = [
        {
            key: "cancel",
            type: "reset",
            onClick: handleClosePopup,
            className: "bg-gray-300 text-(--text-primary)",
            label: "Cancel",
        },
        {
            key: getPopupButton()?.key ?? "unknown",
            type: getPopupButton()?.type ?? "button",
            onClick: getPopupButton()?.onClick,
            className: getPopupButton()?.className ?? "",
            label: getPopupButton()?.label ?? "Unknown",
        },
    ];

    return (
        <Popup isOpen={isOpen} onClose={handleClosePopup}>
            <Popup.Header>
                {getPopupData()?.title || "Unknown"}
                {getPopupData()?.description || "Unknown"}
            </Popup.Header>
            <Popup.Body>
                {getPopupData()?.content || "Unknown"}
                {getPopupData()?.content && (
                    <div className="flex items-center justify-end gap-4">
                        {BUTTON_LIST.map((button) => (
                            <button key={button.key} type={button.type}
                                onClick={button.onClick}
                                className={`${button.className} cursor-pointer py-2 px-4`}
                            >
                                <span>{button.label}</span>
                            </button>
                        ))}
                    </div>
                )}
            </Popup.Body>
        </Popup>
    );
};

interface TreeNodeProps extends NodeRendererProps<TreeNodeModel>, TreeHooks<TreeNodeModel> {
    popupContent: React.ReactNode;
    renderIcon?: TreeIconRender;
    handleSelectNodeLabel: (nodeLabel: TreeNodeType) => void;
    handleSelectActionType: (actionType: OpenType) => void;
};

export function TreeNode({
    node,
    style,
    renderIcon,
    popupContent,
    onAdd,
    onUpdate,
    onDelete,
    handleSelectNodeLabel,
    handleSelectActionType,
}: TreeNodeProps) {
    const [selectedNode, setSelectedNode] = useState<string | null>(null);
    const [openType, setOpenType] = useState<OpenType | null>(null);
    const [isOpen, setIsOpen] = useState(false);

    const { name, isFirst, isLast } = node.data;

    const toggleNode = () => {
        const hasChildren = node?.children;
        if (hasChildren) node.toggle();
        else return;
    };

    const handleSelectNode = () => {
        console.log('Run')
        console.log(selectedNode)
        handleSelectNodeLabel(node.data.type as TreeNodeType);
        setSelectedNode((prev) => (prev === node.id ? null : node.id));
    };

    const handleOpenPopup = (key: OpenType) => {
        handleSelectActionType(key);
        setOpenType(key);
        setIsOpen(true);
    };
    const handleClosePopup = () => {
        setOpenType(null);
        setIsOpen(false);
    };

    const popupButtonAction = { onAdd, onUpdate, onDelete };

    return (
        <div
            style={style}
            className={`flex items-center justify-between ${selectedNode === node.id ? "bg-(--bg-primary)" : "hover:bg-(--bg-primary)"}`}
            onDoubleClick={toggleNode}
            onClick={handleSelectNode}
        >
            <div className="flex items-center gap-2">
                {renderIcon?.(node.data)}
                <span className="font-medium">{name}</span>
            </div>

            <div className="flex gap-2 items-center justify-start mr-4">
                {!isLast && (
                    <button type="button" title="Add"
                        onClick={() => handleOpenPopup("create")}
                        className="text-xs text-indigo-600 cursor-pointer"
                    >
                        <PlusIcon />
                    </button>
                )}

                {(!isLast && !isFirst) && (
                    <button type="button" title="Edit"
                        onClick={() => handleOpenPopup("update")}
                        className="text-xs text-gray-600 cursor-pointer"
                    >
                        <EditIcon />
                    </button>
                )}

                {!isFirst && (
                    <button type="button" title="Delete"
                        onClick={() => handleOpenPopup("delete")}
                        className="text-xs text-red-600 cursor-pointer"
                    >
                        <DeleteIcon />
                    </button>
                )}
            </div>

            {(isOpen && openType)
                && <PopupSection
                    isOpen={isOpen}
                    openType={openType}
                    handleClosePopup={handleClosePopup}
                    content={popupContent}
                    node={node}
                    buttonAction={popupButtonAction}
                />}
        </div>
    );
};