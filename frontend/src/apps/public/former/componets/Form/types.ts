export interface BaseControlProps {
    label?: string;
    placeholder?: string;
    disabled?: boolean;
    required?: boolean;
    error?: string;
    className?: string;
    isFocus?: boolean;
}

export interface DropdownOption {
    label: string;
    value: string;
}

export interface DropdownAction {
    icon: React.ReactNode;
    onClick: () => void;
    tooltip?: string;
}

