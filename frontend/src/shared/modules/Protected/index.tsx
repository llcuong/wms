import { FC, ReactNode } from "react";
import { useAuthStore } from "@modules/Authentication/useAuthStore";
import { Login } from "@modules/Authentication";

interface ProtectedProps {
    children: ReactNode;
}

export const Protected: FC<ProtectedProps> = ({ children }) => {
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    if (!isAuthenticated) {
        return <Login />;
    }

    return <>{children}</>;
};
