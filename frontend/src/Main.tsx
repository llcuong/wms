import React from "react";
import { createRoot } from "react-dom/client";
import { useAppNavigation } from "@routes/navigation";
import { APPS_MAP } from "@routes/configs";
import { Protected } from "@modules/Authentication";
import { ToastProvider } from "@components/toast";
import { ModalProvider } from "@components/modal";
import "@modules/i18next";
import "./global.css"

const Main: React.FC = () => {
    const { currentApp, navigateApp } = useAppNavigation();

    const CurrentApp = APPS_MAP[currentApp];

    if (!CurrentApp) return null;

    return (
        <Protected>
            <CurrentApp
                navigateApp={navigateApp}
                currentApp={currentApp}
            />
        </Protected>
    );
};

const container = document.getElementById("root");
if (container) {
  createRoot(container).render(
    <React.StrictMode>
      <ModalProvider>
        <ToastProvider>
          <Main />
        </ToastProvider>
      </ModalProvider>
    </React.StrictMode>
  );
}