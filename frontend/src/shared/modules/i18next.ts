import i18next from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./Translation/translation.en.json";
import vi from "./Translation/translation.vi.json";
import zhCN from "./Translation/translation.zhCN.json";
import zhTW from "./Translation/translation.zhTW.json";

i18next.use(initReactI18next).init({
    fallbackLng: "en",
    supportedLngs: ["en", "zh-CN", "zh-TW", "vi"],
    interpolation: { escapeValue: false },
    resources: {
        en: { translation: en },
        vi: { translation: vi },
        "zh-CN": { translation: zhCN },
        "zh-TW": { translation: zhTW },
    },
});