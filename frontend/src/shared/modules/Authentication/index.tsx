import { FC } from "react";
import { useAuthStore } from "./useAuthStore";
import { Login } from "./Login";
import type { ProtectedProps } from "./types";

export const Protected: FC<ProtectedProps> = ({ children }) => {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    if (!isAuthenticated) {
        return <Login />;
    }

    return <>{children}</>;
};
