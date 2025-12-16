import { FC } from "react";
import { APPS_CONFIG } from "@routes/configs";
import type { PageNavigatorProps } from "@routes/types";

export interface SidebarProps extends PageNavigatorProps {
    isSideBarOpen: boolean;
    setSideBarOpen: (value: boolean | ((prev: boolean) => boolean)) => void;
}

const BodyTop: FC<SidebarProps> = (props) => {

    const handleOnClick = (appId: number) => {
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

    return (
        <div className="flex-1 min-h-0 overflow-hidden px-1.5 pt-2 space-y-0.5">
            {APPS_CONFIG
                .map((app) => {
                    const Icon = app.icon;
                    const isActive = props.currentApp === app.id;

                    return (
                        <button
                            key={app.id}
                            type="button"
                            onClick={() => handleOnClick(app.id)}
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
                                    {app.name}
                                </span>
                            )}
                        </button>
                    );
                })}
        </div>
    );
};

export default BodyTop;