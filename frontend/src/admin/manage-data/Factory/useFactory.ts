import { useCallback, useEffect, useState } from "react";

import { FactoryNode, TreeNodeType } from "./factoryModel.types";
import { OpenType, TreeNodeModel } from "./Tree/tree.types";

import axiosClient from "@modules/api";
import { createDummyRoot, factoryTreeToGeneric } from "./factoryModel.utils";

export default function useFactory() {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [factoryTree, setFactoryTree] = useState<TreeNodeModel[] | []>([]);

    const [nodeLabel, setNodeLabel] = useState<TreeNodeType | null>(null);
    const [actionType, setActionType] = useState<OpenType | null>(null);

    const getFactoryModelData = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await axiosClient.get("/data-model/get-factory-tree/");
            const rawData: FactoryNode[] = response.data;
            if (Array.isArray(rawData)) {
                const { tree } = factoryTreeToGeneric(rawData);
                const treeWithDummyRoot = createDummyRoot(tree);
                setFactoryTree(treeWithDummyRoot);
            }
        } catch {
            setError("Internal Server Error! Cannot get data!");
        } finally {
            setIsLoading(false);
        };
    }, []);

    useEffect(() => {
        getFactoryModelData();
    }, [getFactoryModelData]);

    const handleSelectNodeLabel = (nodeLabel: TreeNodeType) => setNodeLabel(nodeLabel);
    const handleSelectActionType = (actionType: OpenType) => setActionType(actionType);

    return {
        isLoading,
        error,
        factoryTree,
        getFactoryModelData,

        nodeLabel,
        handleSelectNodeLabel,
        actionType,
        handleSelectActionType,
    };
};