import { Children, isValidElement, ReactElement, ReactNode } from "react";

function isSlotElement(
    child: unknown
): child is ReactElement<{ children?: ReactNode }> {
    return isValidElement(child);
};

interface DropdownSlots {
    left: ReactNode;
    right: ReactNode;
}

export function useSlots(children: ReactNode): DropdownSlots {
    let left: ReactNode = null;
    let right: ReactNode = null;

    Children.forEach(children, (child) => {
        if (!isSlotElement(child)) return;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const displayName = (child.type as any).displayName as string | undefined;

        switch (displayName) {
            case "Dropdown.Left":
                left = child.props.children;
                break;
            case "Dropdown.Right":
                right = child.props.children;
                break;
        }
    });

    return { left, right };
}