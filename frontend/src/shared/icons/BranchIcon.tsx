import { FC, SVGProps } from "react";

export const BranchIcon: FC<SVGProps<SVGSVGElement>> = (props) => (
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
        <circle cx="12" cy="6" r="2" />
        <path d="M12 8v4" />
        <path d="M12 12l-4 4" />
        <path d="M12 12l4 4" />
        <rect x="2" y="18" width="6" height="3" rx="0.5" />
        <rect x="16" y="18" width="6" height="3" rx="0.5" />
    </svg>
);