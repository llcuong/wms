import type { AppNavigatorComponent, PageNavigationMap } from "@routes/types";
import { usePageNavigation } from "@routes/navigation";
import AddBasketPage from "./AddBasket/AddBasketPage";


const NAVIGATE: PageNavigationMap = {
  "add-basket": AddBasketPage,
};

export const Navigate: AppNavigatorComponent = (props) => {
  const { Current, propsApp } = usePageNavigation(
    props.currentApp,
    props.navigateApp,
    NAVIGATE,
    AddBasketPage
  );

  return <Current {...propsApp} />;
};
