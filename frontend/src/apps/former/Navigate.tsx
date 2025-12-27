import type { AppNavigatorComponent, PageNavigationMap } from "@routes/types";
import { usePageNavigation } from "@routes/navigation";
import AddBasketPage from "./AddBasket/AddBasketPage";

import Index from "./Index";

const NAVIGATE: PageNavigationMap = {
  index: Index,
  "add-basket": AddBasketPage,
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
