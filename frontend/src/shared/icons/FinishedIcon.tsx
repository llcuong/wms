import type { FC, SVGProps } from "react";

const FinishedIcon: FC<SVGProps<SVGSVGElement>> = (props) => {
    return (
        <svg
            className="w-6.5 h-6.5 shrink-0"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            {...props}
        >
            <path fill="currentColor" fillRule="evenodd" clipRule="evenodd" d="M12 3.66333L20.25 7.7398V17.01L12 21.0865L3.75 17.01V7.7398L12 3.66333ZM5.25 9.41292V16.078L11.25 19.0427V12.3776L5.25 9.41292ZM12.75 12.3776V19.0427L18.75 16.078V9.41292L16.5 10.5247V13.4999L15 14.2499V11.2659L12.75 12.3776ZM17.807 8.20577L15.8527 9.17139C15.8099 9.13606 15.7624 9.10498 15.7106 9.07908L10.1015 6.27454L12 5.33645L17.807 8.20577ZM8.41452 7.1081L14.1871 9.9944L12 11.0751L6.19304 8.20577L8.41452 7.1081Z"/>
        </svg>
    );
};

export default FinishedIcon;