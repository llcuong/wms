import { ReactNode, useMemo } from "react";
import { useSlots } from "./useSlots";
import { createSlot } from "../../layouts/Navbar/createSlots";
import DropdownPattern from "./DropdownPattern";
import DropdownTrigger from "./DropdownTrigger";
import useDropdown from "./useDropdown";
import { useTranslation } from "react-i18next";

export interface DropdownOption<T> {
    value: T;
    label: string;
};

interface DropdownProps<T = string> {
    optionList: DropdownOption<T>[];
    value: DropdownOption<T> | undefined;
    onChange?: (option: DropdownOption<T>) => void;
    children?: ReactNode;
    offset?: number;
    className?: string;
    align?: 'left' | 'right';
    placeholder?: string;
};

const Dropdown = Object.assign(
    <T,>({
        optionList,
        value,
        onChange,
        children,
        offset = 45,
        className = 'w-30',
        align = 'left',
        placeholder = 'Select options...'
    }: DropdownProps<T>) => {
        const { t } = useTranslation();
        const { left, right } = useSlots(children);

        const {
            selectedOption,
            isOpen,
            ref,
            handleSelectOption,
            toggle,
            close
        } = useDropdown({ onChange, value });

        const renderedOptionList = useMemo(() => {
            return optionList.map((opt: DropdownOption<T>, idx: number) => {
                const isSelected = selectedOption?.value === opt.value;

                return (
                    <div
                        key={idx}
                        onClick={() => handleSelectOption(opt)}
                        className={`px-4 py-2 cursor-pointer
                                    flex items-center gap-2
                                    ${isSelected
                                ? 'bg-(--btn-primary) text-(--text-secondary)'
                                : 'hover:bg-(--color-primary) text-(--text-primary)'}`}
                    >
                        <div className="flex items-center gap-2 flex-1 min-w-0">
                            {left}
                            <span className="truncate">{t(opt.label)}</span>
                        </div>

                        {right && (
                            <div className="flex items-center flex-none">
                                {right}
                            </div>
                        )}
                    </div>
                );
            });
        }, [left, right, optionList, selectedOption, handleSelectOption, t]);

        return (
            <div ref={ref}>
                <DropdownTrigger isOpen={isOpen}
                    onClick={toggle}
                    placeholder={placeholder}
                    selectedOptionLabel={selectedOption?.label || 'No option'}
                    className={className}
                />

                <DropdownPattern isOpen={isOpen} ref={ref}
                    onClose={close}
                    align={align}
                    offset={offset}
                    className={className}
                >
                    <div className="py-1">
                        {renderedOptionList}
                    </div>
                </DropdownPattern>
            </div>
        );
    },
    {
        Left: createSlot("Dropdown.Left"),
        Right: createSlot("Dropdown.Right"),
    }
);

export default Dropdown;