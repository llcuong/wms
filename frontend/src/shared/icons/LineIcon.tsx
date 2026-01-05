import { FC, SVGProps } from "react";

export const LineIcon: FC<SVGProps<SVGSVGElement>> = (props) => (
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
        <rect x="2" y="14" width="20" height="4" rx="2" />
        <rect x="4" y="6" width="4" height="6" rx="1" />
        <rect x="10" y="6" width="4" height="6" rx="1" />
        <rect x="16" y="6" width="4" height="6" rx="1" />
        <path d="M6 12v2" />
        <path d="M12 12v2" />
        <path d="M18 12v2" />
    </svg>
);