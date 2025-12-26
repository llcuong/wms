import { FC } from "react";
import { useTranslation } from "react-i18next";

import type { SidebarProps } from "./types";

import { PRIVATE_CONFIGS } from "@routes/configs";

const BodyBottom: FC<SidebarProps> = (props) => {
    const { t } = useTranslation();

    const extraApps = props.extraPrivateApps ?? [];

    const handleAppClick = (appId: number) => {
        if (props.currentApp === appId) {
            if (typeof props.navigatePage === "function") {
                props.navigatePage("index");
            } else {
                props.navigateApp(appId);
            }
        } else {
            props.navigateApp(appId);
        }
    };

    const handlePageClick = (pageId: string) => {
        if (typeof props.navigatePage === "function") {
            props.navigatePage(pageId);
        }
    };

    return (
        <div className="px-1.5 pb-2 flex flex-col space-y-0.5">
            {PRIVATE_CONFIGS.map((app) => {
                const Icon = app.icon;
                const isActive = props.currentApp === app.id;

                return (
                    <button
                        key={app.id}
                        type="button"
                        onClick={() => handleAppClick(app.id)}
                        className={`w-full h-10 rounded-lg flex items-center transition-colors ${isActive
                            ? "text-(--bg-primary) bg-(--color-primary)"
                            : "text-(--text-primary) hover:text-(--color-primary)"
                            }`}
                    >
                        <div className="ml-2">
                            <Icon />
                        </div>

                        {props.isSideBarOpen && (
                            <span className="font-medium overflow-hidden whitespace-nowrap ml-2.5 text-base">
                                {t(`app.${app.name}`)}
                            </span>
                        )}
                    </button>
                );
            })}
        </div>
    );
};

export default BodyBottom;