import { Navbar, Sidebar, UserMenu } from "@layouts";
import { useSidebarState } from "@hooks";
import { PageNavigatorProps, ExtraAppConfig } from "@routes/types";
import { FC, ReactNode, useMemo } from "react";
import { SettingIcon } from "@icons";
import { NavDropdownGroup, NavDropdown } from "@layouts/Navbar/navDropdown";

interface AppBaseProps extends PageNavigatorProps {
  children?: ReactNode;
}

export const Base: FC<AppBaseProps> = (props) => {
  const { isSideBarOpen, setSideBarOpen } = useSidebarState();

  const navDropdown: NavDropdownGroup[] = [
    {
      label: "Basket",
      icon: <SettingIcon className="w-4 h-4 mr-2" />,
      items: [
        { label: "Add Basket", navigate: "add-basket" },
        { label: "Search Basket", navigate: "search-basket" },
        { label: "Modify Basket", navigate: "modify-basket" },
      ],
    },
    {
      label: "Former",
      icon: <SettingIcon className="w-4 h-4 mr-2" />,
      items: [
        { label: "Add Former", navigate: "add-former" },
        { label: "Search Former", navigate: "search-former" },
        { label: "Former Stock In", navigate: "former-stock-in" },
        { label: "Former Stock Out", navigate: "former-stock-out" },
      ],
    },
    {
      label: "Transaction",
      icon: <SettingIcon className="w-4 h-4 mr-2" />,
      items: [
        {
          label: "Batch Transaction Report",
          href: "/former/batch-transaction-report",
        },
        { label: "Broken Basket Report", navigate: "broken-basket-report" },
        { label: "Broken Former Report", navigate: "broken-former-report" },
      ],
    },
  ];

  //   const navDropdown = [
  //     {
  //       label: "Baskets",
  //       icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //       items: [
  //         {
  //           label: "Add Baskets",
  //           href: "/former/add-baskets",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Search Baskets",
  //           href: "/former/search-baskets",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Modify Baskets",
  //           href: "/former/modify-baskets",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //       ],
  //     },
  //     {
  //       label: "Formers",
  //       icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //       items: [
  //         {
  //           label: "Add Former",
  //           href: "/former/add-former",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Search Former",
  //           href: "/former/search-former",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Former Stock In",
  //           href: "/former/former-stock-in",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Former Stock Out",
  //           href: "/former/former-stock-out",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //       ],
  //     },
  //     {
  //       label: "Transactions",
  //       icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //       items: [
  //         {
  //           label: "Batch Transaction Report",
  //           href: "/former/batch-transaction-report",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Broken Basket Report",
  //           href: "/former/broken-basket-report",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //         {
  //           label: "Broken Former Report",
  //           href: "/former/broken-former-report",
  //           icon: <SettingIcon className="w-4 h-4 mr-2" />,
  //         },
  //       ],
  //     },
  //   ];

  return (
    <>
      <Navbar>
        <Navbar.Left>
          <div className="flex items-center justify-center gap-[20px]">
            <span className="text-(--color-primary) text-xl font-bold">
              Formers
            </span>

            <div className="flex gap-2">
              {navDropdown.map((group) => (
                <NavDropdown
                  key={group.label}
                  group={group}
                  onNavigate={props.navigatePage}
                />
              ))}
            </div>
          </div>
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

      <main
        className={`flex-1 pt-14 transition-all duration-300 ${
          isSideBarOpen ? "ml-56" : "ml-14"
        }`}
      >
        <div className="p-4">{props.children}</div>
      </main>
    </>
  );
};
