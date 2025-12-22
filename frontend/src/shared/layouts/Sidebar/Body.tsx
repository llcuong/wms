import { FC } from "react";
import BodyTop from "./BodyTop";
import BodyBottom from "./BodyBottom";
import type { SidebarProps } from "./types"

export const Body: FC<SidebarProps> = (props) => {
    return (
        <div className="flex-1 w-full flex flex-col min-h-0">
            <BodyTop
                currentApp={props.currentApp}
                navigateApp={props.navigateApp}
                navigatePage={props.navigatePage}
                isSideBarOpen={props.isSideBarOpen}
                setSideBarOpen={props.setSideBarOpen}
            />

            <div className="mt-auto">
                <BodyBottom
                    currentApp={props.currentApp}
                    navigateApp={props.navigateApp}
                    navigatePage={props.navigatePage}
                    isSideBarOpen={props.isSideBarOpen}
                    setSideBarOpen={props.setSideBarOpen}
                />
            </div>

        </div>
    );
};
