import { JSX } from "react";

import type { HREFDataModelType } from "./dataModels.type";

export type DataModelRendererProps = {
    treeData?: any;
};

export const DATA_MODEL_REGISTRY: Record<
    HREFDataModelType,
    {
        label: string;
        render: () => JSX.Element;
    }
> = {
    "#factory": {
        label: "factory",
        render: () => <TreeStructure />,
    },

    "#product": {
        label: "product",
        render: () => <TreeStructure />,
    },
};