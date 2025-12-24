import { useTranslation } from "react-i18next";
import DropdownIcon from "@icons/DropdownIcon";

interface DropdownTriggerProps {
    isOpen: boolean;
    placeholder: string;
    selectedOptionLabel: string;
    onClick: () => void;
    className?: string;
    disabled?: boolean;
};

export default function DropdownTrigger({
    isOpen,
    placeholder,
    selectedOptionLabel,
    onClick,
    className = '',
    disabled = false,
}: DropdownTriggerProps) {
    const { t } = useTranslation();

    return (
        <button type="button"
            onClick={onClick}
            disabled={disabled}
            className={`inline-flex items-center justify-between gap-2 px-4 py-2 border rounded-md
                        bg-(--bg-secondary) hover:text-(--text-primary) focus:text-(--text-third)
                        text-(--text-secondary) disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer
                        transition-colors ${className}`}
        >
            <span>{t(selectedOptionLabel) || placeholder}</span>
            <DropdownIcon isOpen={isOpen} />
        </button>
    );
};