import { FC, ReactNode } from "react";

import { useSidebarState } from "@hooks"
import { PageNavigatorProps } from "@routes/types";
import { Navbar, Sidebar, UserMenu } from "@layouts";

interface AppBaseProps extends PageNavigatorProps {
    children?: ReactNode;
}

export const Base: FC<AppBaseProps> = (props) => {
    const { isSideBarOpen, setSideBarOpen } = useSidebarState();

    return (
        <div className="min-h-screen bg-(--bg-secondary)">
            <Navbar>
                <Navbar.Left>
                    <span className="text-(--color-primary) text-xl font-bold">
                        Finished Goods
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

            <main className={`relative flex-1 transition-all duration-300 ${isSideBarOpen ? "ml-56" : "ml-14"}`}>
                {props.children}
            </main>
        </div>
    );
};