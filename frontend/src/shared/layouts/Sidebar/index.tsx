import { ToggleButton } from "./ToggleButton";
import { Body } from "./Body";
import { type SidebarProps } from "./BodyTop";

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
            />

            <div className="w-full flex justify-center">
                <div className="w-10 h-0.5 bg-gray-200 rounded" />
            </div>
            <div className="h-10 w-full flex flex-col justify-center cursor-pointer">

            </div>

        </aside>
    );
};
