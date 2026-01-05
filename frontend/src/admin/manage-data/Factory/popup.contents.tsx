import React from "react";

import { OpenType } from "./Tree/tree.types";
import { TreeNodeType } from "./factoryModel.types";

interface PopupContentProps {
    nodeLabel: TreeNodeType | null;
    actionType: OpenType | null;
};

export const PopupContent = ({
    nodeLabel,
    actionType,
}: PopupContentProps) => {
    if (actionType && nodeLabel)
        return POPUP_CONTENT_MAP[actionType]?.[nodeLabel];
    else return undefined;
};

const DeleteContent = ({ nodeLabel }: { nodeLabel: TreeNodeType }) => {
    const getData = () => {
        switch (nodeLabel) {
            case "factory":
                break;
            case "branch":
                break;
            case "machine":
                break;
            case "line":
                break;
        };
    };

    return (
        <div></div>
    );
};

// ==================================================
// Factory
// ==================================================
const FactoryCreateContent = () => {
    return (
        <div>Create Factory</div>
    );
};

const FactoryUpdateContent = () => {
    return (
        <div>Update Factory</div>
    );
};

// ==================================================
// Branch
// ==================================================
const BranchCreateContent = () => {
    return (
        <div>Create Branch</div>
    );
};

const BranchUpdateContent = () => {
    return (
        <div>Update Branch</div>
    );
};

// ==================================================
// Machine
// ==================================================
const MachineCreateContent = () => {
    return (
        <div>Create Machine</div>
    );
};

const MachineUpdateContent = () => {
    return (
        <div>Update Machine</div>
    );
};

// ==================================================
// Line
// ==================================================
const LineCreateContent = () => {
    return (
        <div>Create Line</div>
    );
};

const LineUpdateContent = () => {
    return (
        <div>Update Line</div>
    );
};

// ==================================================
// Mapper
// ==================================================
const POPUP_CONTENT_MAP: Record<
    OpenType,
    Partial<Record<TreeNodeType, React.ReactNode>>
> = {
    create: {
        root: <FactoryCreateContent />,
        factory: <BranchCreateContent />,
        branch: <MachineCreateContent />,
        machine: <LineCreateContent />,
    },
    update: {
        factory: <FactoryUpdateContent />,
        branch: <BranchUpdateContent />,
        machine: <MachineUpdateContent />,
        line: <LineUpdateContent />,
    },
    delete: {
        factory: <DeleteContent nodeLabel="factory" />,
        branch: <DeleteContent nodeLabel="branch" />,
        machine: <DeleteContent nodeLabel="machine" />,
        line: <DeleteContent nodeLabel="line" />,
    },
};