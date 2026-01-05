import { useTranslation } from "react-i18next";

import type { PageNavigatorComponent } from "@routes/types";

import { Base } from "./Base";
import { DATA_MODEL_LIST } from "./dataModels.registry";
import useManageData from "./useManageData";

const Index: PageNavigatorComponent = (props) => {
    const { t } = useTranslation();

    const {
        selectedDataModel,
        setSelectedDataModel,
    } = useManageData();

    const getDataModelContent = () => {
        const dataModel = DATA_MODEL_LIST.find(model => model.id === selectedDataModel) ?? undefined;
        if (dataModel) return (
            <div className="h-[70vh] mt-2 pl-4 overflow-auto" id={dataModel.id}>
                {dataModel?.render}
            </div>
        );
        else return;
    };

    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}
        >
            <div className="bg-(--bg-primary)) container mx-auto px-4 py-2">
                <div className="mb-4">
                    <h1 className="text-3xl font-bold bg-(--color-primary) bg-clip-text text-transparent">
                        {t("title.dataModels")}
                    </h1>
                    <p className="text-(--text-secondary) mt-1">{t("description.dataModels")}</p>
                </div>

                <nav className="bg-(--color-secondary)">
                    {/* Data model apps */}
                    <ul className="flex items-center justify-start border-b py-2">
                        {DATA_MODEL_LIST.map((dataModel, idx) => (
                            <li key={idx} className="">
                                <a href={dataModel.id}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        setSelectedDataModel(dataModel.id);
                                    }}
                                    className={`relative px-4 py-2 transition-all duration-300
                                                after:absolute after:left-0 after:right-0 after:-bottom-0.5 after:h-0.5 after:bg-current after:scale-x-0 after:origin-left 
                                                focus:after:scale-x-100 focus:text-(--color-primary)
                                                hover:text-(--color-primary)
                                                ${selectedDataModel === dataModel.id
                                            ? "text-(--color-primary) after:scale-x-100"
                                            : "after:scale-x-0"
                                        }`}
                                >
                                    {t(`dataModel.${dataModel.label}`)}
                                </a>
                            </li>
                        ))}
                    </ul>
                </nav>

                <div className="relative w-full h-full bg-(--color-secondary)">
                    {getDataModelContent()}
                </div>
            </div>
        </Base>
    );
};

export default Index;