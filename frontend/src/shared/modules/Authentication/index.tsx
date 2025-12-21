import { FC, ReactNode } from "react";
import { useAuthStore } from "./useAuthStore";
import { Login } from "./Login";

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
