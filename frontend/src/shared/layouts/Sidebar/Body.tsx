import { FC } from "react";
import BodyTop, { type SidebarProps } from "./BodyTop";

export const Body: FC<SidebarProps> = (props) => {
    return (
        <div className="flex-1 w-full flex flex-col">
            <BodyTop
                currentApp={props.currentApp}
                navigateApp={props.navigateApp}
                navigatePage={props.navigatePage}
                isSideBarOpen={props.isSideBarOpen}
                setSideBarOpen={props.setSideBarOpen}
            />
        </div>
    );
};
