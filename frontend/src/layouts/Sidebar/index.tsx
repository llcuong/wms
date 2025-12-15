import { useState } from "react";
import { ToggleButton } from "./ToggleButton";
import Body from "./Body";
import { type PageNavigatorProps } from "@routes/types";

export const Sidebar = (props: PageNavigatorProps) => {
    const [isSideBarOpen, setSideBarOpen] = useState(false);
    const toggleSidebar = () => setSideBarOpen((prev) => !prev);

    return (
        <aside
            className={`bg-(--bg-primary) fixed top-14 bottom-0 z-1 shadow-xl flex flex-col py-2 transition-[width,transform] duration-300 ease-out border border-(--color-secondary)
            ${isSideBarOpen ? "w-56 items-start" : "w-14 items-center"}`}
        >
            <ToggleButton
                toggleSidebar={toggleSidebar}
                isSideBarOpen={isSideBarOpen}
            />

            <Body
                currentApp={props.currentApp}
                navigateApp={props.navigateApp}
                navigatePage={props.navigatePage}
                isSideBarOpen={isSideBarOpen}
            />
        </aside>
    );
};
