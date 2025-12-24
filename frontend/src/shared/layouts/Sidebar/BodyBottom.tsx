import { FC } from "react";
import type { SidebarProps } from "./types";
import { ADMIN_CONFIGS } from "@routes/configs";

const BodyBottom: FC<SidebarProps> = (props) => {

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

    return (
        <div className="px-1.5 pb-2 flex flex-col space-y-0.5">
            <div className="mb-0.5">
                {props.isSideBarOpen && (
                    <>
                        <div className="w-full flex justify-center">
                            <div className="w-10 h-0.5 bg-gray-200 rounded" />
                        </div>
                        <span className={'text-sm pl-1 font-medium text-gray-500'}>
                            Admin
                        </span>
                    </>
                )}
            </div>
            <div className={`border-l-3 ${props.isSideBarOpen ? 'border-l-gray-200' : 'border-l-white'}`}>
                {ADMIN_CONFIGS.map((app) => {
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
                                    {app.name}
                                </span>
                            )}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default BodyBottom;
