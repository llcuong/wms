import { FC, SVGProps } from "react";

export const MachineIcon: FC<SVGProps<SVGSVGElement>> = (props) => (
    <svg
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        stroke="currentColor"
        strokeWidth={1.5}
        strokeLinecap="round"
        strokeLinejoin="round"
        {...props}
    >
        <rect x="3" y="7" width="18" height="10" rx="2" />
        <circle cx="8" cy="12" r="1" />
        <circle cx="12" cy="12" r="1" />
        <path d="M15 7V4h4" />
        <path d="M6 17v3" />
        <path d="M18 17v3" />
    </svg>
);