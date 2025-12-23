import React from "react";
import { createRoot } from "react-dom/client";
import { useAppNavigation } from "@routes/navigation";
import { APPS_MAP } from "@routes/configs";
import { Protected } from "@modules/Authentication";
import "./global.css"

const Main: React.FC = () => {
    const { currentApp, navigateApp } = useAppNavigation();

    const CurrentApp = APPS_MAP[currentApp];

    if (!CurrentApp) return null;

    return (
        <CurrentApp
            navigateApp={navigateApp}
            currentApp={currentApp}
        />
    );
};

const container = document.getElementById("root");
if (container) {
    const root = createRoot(container);
    root.render(<Main />);
}