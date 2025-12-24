import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { LANG } from "@routes/configs";
import { LANGUAGE_OPTION_LIST } from "./languageOptionList";

export default function useLang() {
    const { i18n } = useTranslation();

    // Initialize selectedLang from localStorage or i18n.language 
    const [selectedLang, setSelectedLang] = useState(
        LANGUAGE_OPTION_LIST.find(lang => lang.value === localStorage.getItem(LANG)) ||
        LANGUAGE_OPTION_LIST[0]
    );

    // Get language in local storage
    useEffect(() => {
        const currentLang = localStorage.getItem(LANG) || undefined;
        if (currentLang !== i18n.language) {
            i18n.changeLanguage(currentLang);
        };
    }, [i18n]);

    // Change language based on user command
    useEffect(() => {
        if (!LANGUAGE_OPTION_LIST.find(lang => lang.value === selectedLang.value)) return;
        i18n.changeLanguage(selectedLang.value);
        localStorage.setItem(LANG, selectedLang.value);
    }, [selectedLang, i18n]);

    return { selectedLang, setSelectedLang };
};