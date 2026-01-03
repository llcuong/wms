import { JSX } from "react";

import FactoryModel from "./Factory";

export type DataModelId = "#factory";

interface DataModel {
    id: DataModelId;
    label: "factory";
    render: JSX.Element;
};

export const DATA_MODEL_LIST: DataModel[] = [
    {
        id: "#factory",
        label: "factory",
        render: <FactoryModel />
    },
];