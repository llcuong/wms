import type { AppNavigatorComponent, PageNavigationMap } from "@routes/types";
import { usePageNavigation } from "@routes/navigation";

import Index from "./Index";
import UsersPage from "./UsersPage";
import AccountsPage from "./AccountsPage";

const NAVIGATE: PageNavigationMap = {
    index: Index,
    users: UsersPage,
    accounts: AccountsPage,
};

export const Navigate: AppNavigatorComponent = (props) => {
    const { Current, propsApp } = usePageNavigation(
        props.currentApp,
        props.navigateApp,
        NAVIGATE,
        Index
    );

    return <Current {...propsApp} />;
};
