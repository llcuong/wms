import type { ReactNode, FC } from "react";

export interface NavbarProps {
    children: ReactNode;
}

export interface NavbarSlots {
    left: ReactNode;
    middle: ReactNode;
    right: ReactNode;
}

export type SlotComponent<P = { children?: ReactNode }> = FC<P> & {
    displayName?: string;
};