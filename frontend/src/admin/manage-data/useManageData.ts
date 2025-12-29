import { useCallback, useEffect, useState } from "react";

import type { HREFDataModelType } from "./dataModels.type";
import { BranchModel, FactoryModel, MachineLineModel, MachineModel } from "./dataModels.type";

import axiosClient from "@modules/api";

const API_ROUTE = {
    API_FACTORY_LIST: "/data-model/get-factory-list/",
    API_BRANCH_LIST: "/data-model/get-branch-list/",
    API_MACHINE_LIST: "/data-model/get-machine-list/",
    API_MACHINE_LINE_LIST: "/data-model/get-machine-line-list/",
};

export default function useManageData() {
    const [selectedDataModel, setSelectedDataModel] = useState<HREFDataModelType>();
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [factoryList, setFactoryList] = useState<FactoryModel>([]);
    const [branchList, setBranchList] = useState<BranchModel>([]);
    const [machineList, setMachineList] = useState<MachineModel>([]);
    const [lineList, setLineList] = useState<MachineLineModel>([]);

    const getDataModelList = useCallback(async (dataModel: string) => {
        try {
            setIsLoading(true);
            switch (dataModel) {
                case "factory":
                    {
                        const response = await axiosClient.get(API_ROUTE.API_FACTORY_LIST);
                        if (response.data) return setFactoryList(response.data);
                        else return error;
                    }
                case "branch":
                    {
                        const response = await axiosClient.get(API_ROUTE.API_BRANCH_LIST);
                        if (response.data) return setBranchList(response.data);
                        else return error;
                    }
                case "machine":
                    {
                        const response = await axiosClient.get(API_ROUTE.API_MACHINE_LIST);
                        if (response.data) return setMachineList(response.data);
                        else return error;
                    }
                case "line":
                    {
                        const response = await axiosClient.get(API_ROUTE.API_MACHINE_LINE_LIST);
                        if (response.data) return setLineList(response.data);
                        else return error;
                    }
                default:
                    return error;
            };
        } catch {
            setError(`Internal Server Error! Cannot get ${dataModel} data!`);
        } finally {
            setIsLoading(false);
        };
    }, [error]);

    useEffect(() => {
        getDataModelList("factory");
        getDataModelList("branch");
        getDataModelList("machine");
        getDataModelList("line");
    }, [getDataModelList]);

    return {
        selectedDataModel,
        setSelectedDataModel,
        isLoading,
        error,

        factoryList,
        branchList,
        machineList,
        lineList,
    };
};