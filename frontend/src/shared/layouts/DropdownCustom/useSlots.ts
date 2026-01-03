import { Children, isValidElement, ReactElement, ReactNode } from "react";

function isSlotElement(
    child: unknown
): child is ReactElement<{ children?: ReactNode }> {
    return isValidElement(child);
};

interface DropdownSlots {
    header: ReactNode;
    body: ReactNode;
    footer: ReactNode;
};

export function useSlots(children: ReactNode): DropdownSlots {
    let header: ReactNode = null;
    let body: ReactNode = null;
    let footer: ReactNode = null;

    Children.forEach(children, (child) => {
        if (!isSlotElement(child)) return;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const displayName = (child.type as any).displayName as string | undefined;

        switch (displayName) {
            case "Dropdown.Header":
                header = child.props.children;
                break;
            case "Dropdown.Body":
                body = child.props.children;
                break;
            case "Dropdown.Footer":
                footer = child.props.children;
                break;
        }
    });

    return { header, body, footer };
};