import type { NavbarProps } from "./types";
import { createSlot } from "./createSlots";
import { useSlots } from "./useSlots";

export const Navbar = Object.assign(
    ({ children }: NavbarProps) => {
        const { left, middle, right } = useSlots(children);

        return (
            <nav className="bg-(--bg-primary) sticky top-0 z-2 border-b border-b-(--color-secondary) shadow-[0_10px_5px_-3px_var(--shadow-primary),0_4px_6px_-2px_var(--shadow-primary)] ">
                <div className="mx-auto px-4">
                    <div className="flex items-center h-14">

                        <div className="flex items-center justify-start gap-1 flex-1 min-w-0">
                            <div className="ml-8 shrink-0">{left}</div>
                        </div>

                        <div className="flex flex-row items-center flex-none mx-4 min-w-0">
                            {middle}
                        </div>

                        <div className="flex items-center justify-end gap-1 flex-1 min-w-0">
                            {right}
                        </div>
                    </div>
                </div>
            </nav>
        );
    },
    {
        Left: createSlot("Navbar.Left"),
        Middle: createSlot("Navbar.Middle"),
        Right: createSlot("Navbar.Right"),
    }
);
