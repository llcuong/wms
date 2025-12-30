import { Navbar, Sidebar, UserMenu } from "@layouts";
import { useSidebarState } from "@hooks"
import { PageNavigatorProps } from "@routes/types";
import { FC, ReactNode } from "react";

interface AppBaseProps extends PageNavigatorProps {
    children?: ReactNode;
}

export const Base: FC<AppBaseProps> = (props) => {
    const { isSideBarOpen, setSideBarOpen } = useSidebarState();

    return (
        <>
            <Navbar>
                <Navbar.Left>
                    <span className="text-(--color-primary) text-xl font-bold">
                        Semi-Finished Goods
                    </span>
                </Navbar.Left>
                <Navbar.Right>
                    <UserMenu />
                </Navbar.Right>
            </Navbar>

            <Sidebar
                currentApp={props.currentApp}
                navigateApp={props.navigateApp}
                navigatePage={props.navigatePage}
                isSideBarOpen={isSideBarOpen}
                setSideBarOpen={setSideBarOpen}
            />

            <main className={`flex-1 pt-14 transition-all duration-300 ${isSideBarOpen ? "ml-56" : "ml-14"}`}>
                <div className="p-4">
                    {props.children}
                </div>
            </main>
        </>
    );
};