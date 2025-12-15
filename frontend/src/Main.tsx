import React from "react";
import { createRoot } from "react-dom/client";
import {useAppNavigation} from "@routes/navigation";
import {APPS_MAP} from "@routes/configs";
import "./global.css"

const Main: React.FC = () => {
    const { currentApp, navigateApp } = useAppNavigation();

    const CurrentComponent = APPS_MAP[currentApp];

    if (!CurrentComponent) return null;

    return (
        <CurrentComponent
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