import { useState } from "react";

import type { DataModelId } from "./dataModels.registry";

export default function useManageData() {
    const [selectedDataModel, setSelectedDataModel] = useState<DataModelId | undefined>(undefined);

    return {
        selectedDataModel,
        setSelectedDataModel,
    };
};