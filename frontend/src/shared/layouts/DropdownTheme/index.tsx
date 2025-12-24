import { FC, useMemo } from "react";
import useTheme, { Theme } from "./useTheme";
import Dropdown, { DropdownOption } from "../Dropdown/Dropdown";

export const DropdownTheme: FC = () => {
    const { themeState, setTheme } = useTheme();

    const themeOptions: DropdownOption<Theme>[] = useMemo(
        () => [
            { value: 'light', label: 'theme.light' },
            { value: 'dark', label: 'theme.dark' },
        ],
        []
    );

    const selectedOption = useMemo(
        () => themeOptions.find(opt => opt.value === themeState),
        [themeOptions, themeState]
    );

    return (
        <Dropdown className="w-24"
            optionList={themeOptions}
            value={selectedOption}
            onChange={(option) => setTheme(option.value)}
        />
    );
};