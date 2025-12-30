import type { AppNavigatorComponent, PageNavigationMap } from "@routes/types";
import { usePageNavigation } from "@routes/navigation";

import Index from "./Index.tsx";

const NAVIGATE: PageNavigationMap = {
    index: Index,
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
