import { useTranslation } from "react-i18next";

import { TreeStructure } from "./Tree";

import { PopupContent } from "./popup.contents";
import { factoryTreeIconRender } from "./factoryModel.icons";
import useFactory from "./useFactory";
import useNestedTree from "./Tree/useNestedTree";

export default function FactoryModel() {
    const { t } = useTranslation();

    const {
        isLoading,
        error,
        factoryTree,
        getFactoryModelData,

        nodeLabel,
        handleSelectNodeLabel,
        actionType,
        handleSelectActionType,
    } = useFactory();

    const {
        data,
        createNode,
        updateNoteById,
        deleteNodeById
    } = useNestedTree(factoryTree);

    if (isLoading) return (
        <div className="flex items-center justify-center py-20 w-full h-full">
            <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin"></div>
                <p className="text-(text-primary) font-medium">{t("status.loading")}</p>
            </div>
        </div>
    );
    if (error) return (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center mt-4 mr-4">
            <div className="text-red-600 font-medium">{error}</div>
            <button type="button"
                onClick={getFactoryModelData}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all duration-300 cursor-pointer"
            >
                {t("button.retry")}
            </button>
        </div>
    );
    if (!factoryTree) return (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 text-center mt-4 mr-4">
            <div className="text-red-600 font-medium">{t("notification.noData")}</div>
        </div>
    );

    return (
        <TreeStructure
            data={data}
            onAdd={createNode}
            onUpdate={(next, prev) => updateNoteById(prev.id, () => next, prev.parentId)}
            onDelete={(node) => deleteNodeById(node.id, node.parentId)}
            renderIcon={factoryTreeIconRender}
            handleSelectNodeLabel={handleSelectNodeLabel}
            handleSelectActionType={handleSelectActionType}
            popupContent={<PopupContent nodeLabel={nodeLabel} actionType={actionType} />}
        />
    );
};