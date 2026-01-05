import { FC, SVGProps } from "react";

export const DeleteIcon: FC<SVGProps<SVGSVGElement>> = (props) => (
    <svg
        className="w-4 h-4"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        stroke="currentColor"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
        {...props}
    >
        <rect
            x="3"
            y="3"
            width="18"
            height="18"
            rx="6"
        />

        <path d="M8 12h8" />
    </svg>
);