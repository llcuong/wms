import { ToggleButton } from "./ToggleButton";
import { Body } from "./Body";
import { Footer } from "./Footer";
import type { SidebarProps } from "./types";

export const Sidebar = ({ isSideBarOpen, setSideBarOpen, ...props }: SidebarProps) => {
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
                setSideBarOpen={setSideBarOpen}
                extraPrivateApps={props.extraPrivateApps}
            />

            <Footer
                isSideBarOpen={isSideBarOpen}
            />
        </aside>
    );
};
