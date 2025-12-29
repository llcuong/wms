import { FC, SVGProps } from "react";

export const FactoryIcon: FC<SVGProps<SVGSVGElement>> = (props) => (
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
        <path d="M3 21V10h4v11" />
        <path d="M7 10l5-3v3l5-3v13H7" />
        <rect x="9" y="14" width="2" height="2" fill="currentColor" stroke="none" />
        <rect x="13" y="14" width="2" height="2" fill="currentColor" stroke="none" />
        <rect x="9" y="18" width="2" height="2" fill="currentColor" stroke="none" />
        <rect x="13" y="18" width="2" height="2" fill="currentColor" stroke="none" />
        <path d="M2 21h20" />
    </svg>
);