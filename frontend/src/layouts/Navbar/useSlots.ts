import { Children, isValidElement, ReactElement, ReactNode } from "react";
import type { NavbarSlots } from "./types";

function isSlotElement(
    child: unknown
): child is ReactElement<{ children?: ReactNode }> {
    return isValidElement(child);
}

export function useSlots(children: ReactNode): NavbarSlots {
    let left: ReactNode = null;
    let middle: ReactNode = null;
    let right: ReactNode = null;

    Children.forEach(children, (child) => {
        if (!isSlotElement(child)) return;

        const displayName = (child.type as any).displayName as string | undefined;

        switch (displayName) {
            case "Navbar.Left":
                left = child.props.children;
                break;
            case "Navbar.Middle":
                middle = child.props.children;
                break;
            case "Navbar.Right":
                right = child.props.children;
                break;
        }
    });

    return { left, middle, right };
}