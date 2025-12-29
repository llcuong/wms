import { useTranslation } from "react-i18next";

import type { PageNavigatorComponent } from "@routes/types";
import type { HREFDataModelType } from "./dataModels.type";
import type { TreeNodeModel } from "./Tree/tree.types";

import { Base } from "./Base";
import { TreeStructure } from "./Tree";
import useManageData from "./useManageData";
import useNestedTree from "./Tree/useNestedTree";

const initialData: TreeNodeModel[] = [
    {
        id: "1",
        name: "Giang Dien",
        code: "gd",
        type: "factory",
        children: [
            {
                id: "gd1", code: "gd-pvc1", name: "PVC1", parentId: "1", type: "branch", children: [
                    {
                        id: "1",
                        name: "Giang Dien",
                        code: "gd",
                        type: "machine",
                    }
                ]
            },
            { id: "gd2", code: "gd-nbr1", name: "NBR1", parentId: "1", type: "branch" },
            { id: "gd3", code: "gd-nbr2", name: "NBR2", parentId: "1", type: "branch" },
        ],
    },
    {
        id: "2",
        name: "Long Khanh",
        code: "lk",
        type: "factory",
        children: [
            { id: "lk1", code: "gd-nbr1", name: "NBR1", parentId: "2", type: "branch" },
            { id: "lk2", code: "gd-nbr2", name: "NBR2", parentId: "2", type: "branch" },
        ],
    },
    {
        id: "3",
        name: "Long Thanh",
        code: "lt",
        type: "factory",
        children: [
            { id: "lt1", code: "gd-pvc1", name: "PVC1", parentId: "3", type: "branch" },
            { id: "lt2", code: "gd-pvc2", name: "PVC2", parentId: "3", type: "branch" },
        ],
    },
];

const Index: PageNavigatorComponent = (props) => {
    const { t } = useTranslation();

    const {
        data,
        createChild,
        renameNode,
        removeNode
    } = useNestedTree(initialData);

    const {
        selectedDataModel,
        setSelectedDataModel,
    } = useManageData();

    const DATA_MODEL_LIST: { label: string, href: HREFDataModelType }[] = [
        {
            label: t("factory"),
            href: "#factory"
        },
        {
            label: t("product"),
            href: "#product"
        },
    ];

    return (
        <Base
            currentApp={props.currentApp}
            navigateApp={props.navigateApp}
            navigatePage={props.navigatePage}
        >
            <div className="bg-(--bg-primary)) container mx-auto px-4 py-8">
                <div className="mb-10">
                    <h1 className="text-3xl font-bold bg-(--color-primary) bg-clip-text text-transparent">
                        {t("title.dataModels")}
                    </h1>
                    <p className="text-(--text-secondary) mt-1">{t("description.dataModels")}</p>
                </div>

                <nav className="bg-(--color-secondary)">
                    {/* Data model apps */}
                    <ul className="flex items-center justify-start border-b py-2">
                        {DATA_MODEL_LIST.map((app, idx) => (
                            <li key={idx} className="">
                                <a
                                    href={app.href}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        setSelectedDataModel(app.href);
                                    }}
                                    className={`relative px-4 py-2 transition-all duration-300
                                                after:absolute after:left-0 after:right-0 after:-bottom-0.5 after:h-0.5 after:bg-current after:scale-x-0 after:origin-left 
                                                focus:after:scale-x-100 focus:text-(--color-primary)
                                                hover:text-(--color-primary)
                                                ${selectedDataModel === app.href
                                            ? "text-(--color-primary) after:scale-x-100"
                                            : "after:scale-x-0"
                                        }`}
                                >
                                    {app.label}
                                </a>

                            </li>
                        ))}
                    </ul>
                </nav>

                <div className="relative w-full h-full bg-(--color-secondary)">
                    {DATA_MODEL_LIST.map((model) =>
                        selectedDataModel === model.href ? (
                            <div
                                key={model.href}
                                id={model.href}
                                className="mt-4 py-2 px-4"
                            >
                                <TreeStructure
                                    data={data}
                                    onAdd={createChild}
                                    onRename={renameNode}
                                    onDelete={removeNode}
                                />
                            </div>
                        ) : null
                    )}
                </div>
            </div>
        </Base>
    );
};

export default Index;