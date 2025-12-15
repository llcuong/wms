import type { FC, SVGProps } from "react";

const HomeIcon: FC<SVGProps<SVGSVGElement>> = (props) => {
    return (
        <svg
            className="w-[22px] h-[22px] shrink-0"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            {...props}
        >
            <g clipPath="url(#clip0_429_11177)">
                <path
                    d="M19 10V19C19 20.1046 18.1046 21 17 21H7C5.89543 21 5 20.1046 5 19V10M21 12L12 3L3 12"
                    stroke="currentColor"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </g>
            <defs>
                <clipPath id="clip0_429_11177">
                    <rect width="24" height="24" fill="white" />
                </clipPath>
            </defs>
        </svg>
    );
};

export default HomeIcon;