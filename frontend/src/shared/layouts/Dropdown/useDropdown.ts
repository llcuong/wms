import { useCallback, useRef, useState } from "react";
import { DropdownOption } from "./Dropdown";

interface useDropdownProps {
    onChange?: (option: DropdownOption) => void;
    value?: DropdownOption;
};

export default function useDropdown({ onChange, value }: useDropdownProps) {
    const [selectedOption, setSelectedOption] = useState<DropdownOption | null>(
        () => value ?? null
    );
    const [isOpen, setIsOpen] = useState(false);

    const ref = useRef<HTMLDivElement | null>(null);

    const toggle = useCallback(() => setIsOpen(prev => !prev), []);
    const close = useCallback(() => setIsOpen(false), []);

    const handleSelectOption = useCallback((option: DropdownOption) => {
        setSelectedOption(option);
        onChange?.(option);
        setIsOpen(false);
    }, [onChange]);

    return {
        selectedOption,
        isOpen,
        ref,
        toggle,
        close,
        handleSelectOption,
    };
};