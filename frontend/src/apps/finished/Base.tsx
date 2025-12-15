import { Navbar, Sidebar } from "@Layouts";
import { PageNavigatorProps } from "@routes/types";

import { FC, ReactNode } from "react";

interface AppBaseProps extends PageNavigatorProps {
    children?: ReactNode;
}

export const Base: FC<AppBaseProps> = (props) => {
    return (
        <>
            <Navbar>
                <Navbar.Left>
                    <span className="text-(--color-primary) text-xl font-bold">
                        Finished Goods
                    </span>
                </Navbar.Left>
            </Navbar>

            <Sidebar
                currentApp={props.currentApp}
                navigateApp={props.navigateApp}
                navigatePage={props.navigatePage}
            />

            <main className="flex-1 pt-14 transition-all duration-300">
                <div className="p-4">
                    {props.children}
                </div>
            </main>
        </>
    );
};