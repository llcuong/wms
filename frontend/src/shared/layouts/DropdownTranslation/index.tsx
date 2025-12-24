import { FC } from "react";
import useLang from "./useLang";
import Dropdown from "../Dropdown/Dropdown";
import { LANGUAGE_OPTION_LIST } from "./languageOptionList";

export const DropdownTranslation: FC = () => {
	const { selectedLang, setSelectedLang } = useLang();

	return (
		<Dropdown className="w-40"
			optionList={LANGUAGE_OPTION_LIST}
			value={selectedLang}
			onChange={setSelectedLang}
		/>
	);
};