interface Props {
    isSideBarOpen: boolean;
    toggleSidebar: () => void;
}

export function ToggleButton({ isSideBarOpen, toggleSidebar }: Props) {
    return (
        <button onClick={toggleSidebar}
            className={`absolute top-[calc(50%-4px)] -right-2.5 w-5 h-5 rounded-full
                       bg-(--color-primary) text-(--bg-primary) shadow ring-2 ring-white/80 transition`}
            aria-expanded={isSideBarOpen} type="button">
            <svg className={`w-3.5 h-3.5 mx-auto transition-opacity ${isSideBarOpen ? "opacity-0 absolute" : "opacity-100"}`}
                viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
            </svg>

            <svg className={`w-5 h-5 mx-auto transition-opacity ${isSideBarOpen ? "opacity-100" : "opacity-0 absolute"}`}
                viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"d="M6 18L18 6M6 6l12 12"/>
            </svg>
        </button>
    );
}
