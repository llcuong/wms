import type { SlotComponent } from "./types";

export function createSlot(name: string): SlotComponent {
    const Slot: SlotComponent = ({ children }) => <>{children}</>;
    Slot.displayName = name;
    return Slot;
}