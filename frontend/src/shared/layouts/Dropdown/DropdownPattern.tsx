import { ReactNode, RefObject, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

interface Position {
    top: number;
    left: number | null;
    right: number | null;
};

interface DropdownProps {
    ref: RefObject<HTMLElement | null>;
    isOpen: boolean;
    onClose: () => void;
    children: ReactNode;
    className?: string;
    offset?: number;
    align?: 'left' | 'right';
    menuId?: string;
    parentMenuId?: string | null;
    ariaLabel?: string;
    zIndex?: number;
};

export default function DropdownPattern({
    ref,
    isOpen,
    onClose,
    children,
    className = '',
    offset = 30,
    align = 'left',
    menuId = `menu-${Math.random().toString(36).substring(2, 9)}`,
    parentMenuId = null,
    ariaLabel,
    zIndex = 30
}: DropdownProps) {
    const [pos, setPos] = useState<Position>({ top: 0, left: null, right: null });
    const [isVisible, setIsVisible] = useState<boolean>(false);
    const menuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (ref.current && !ref.current.dataset.triggerId) {
            ref.current.dataset.triggerId = menuId;
        }
    }, [ref, menuId]);

    // Calculate and update menu position
    useEffect(() => {
        if (!isOpen) return;

        const updatePosition = () => {
            if (ref.current) {
                const rect = ref.current.getBoundingClientRect();
                const menuWidth = menuRef.current?.offsetWidth || 0;
                const viewportWidth = window.innerWidth;

                const positionStyle: Position = { top: rect.top + window.scrollY + offset, left: null, right: null };

                if (align === 'right') {
                    // Calculate right position
                    const right = viewportWidth - (rect.right + window.scrollX);

                    // Check if menu would overflow on the left side
                    if (rect.right - menuWidth < 0) {
                        // Switch to left alignment if overflowing
                        positionStyle.left = Math.max(10, rect.left + window.scrollX);
                        positionStyle.right = null;
                    } else {
                        positionStyle.right = Math.max(10, right);
                        positionStyle.left = null;
                    }
                } else {
                    // Calculate left position
                    const left = rect.left + window.scrollX;

                    // Check if menu would overflow on the right side
                    if (left + menuWidth > viewportWidth) {
                        // Switch to right alignment if overflowing
                        const right = viewportWidth - (rect.right + window.scrollX);
                        positionStyle.right = Math.max(10, right);
                        positionStyle.left = null;
                    } else {
                        positionStyle.left = Math.max(10, left);
                        positionStyle.right = null;
                    }
                }

                setPos(positionStyle);
            }
        };

        updatePosition();
        const timer = setTimeout(() => setIsVisible(true), 10);

        window.addEventListener('scroll', updatePosition, true);
        window.addEventListener('resize', updatePosition);

        return () => {
            clearTimeout(timer);
            window.removeEventListener('scroll', updatePosition, true);
            window.removeEventListener('resize', updatePosition);
        };
    }, [ref, isOpen, offset, align]);

    // Close menu when clicking outside
    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (event: MouseEvent) => {
            if (menuRef.current && menuRef.current?.contains(event.target as Node)) return;
            if (ref.current && ref.current?.contains(event.target as Node)) return;

            // Check if clicking inside a child menu
            const clickedMenu = (event.target as HTMLElement).closest('[role="menu"]');
            if (clickedMenu) {
                const clickedParentId = clickedMenu.getAttribute('data-parent-id');
                const clickedMenuId = clickedMenu.getAttribute('data-menu-id');

                // Don't close if clicking inside a child menu of this menu
                if (clickedParentId === menuId) return;

                // Don't close if clicking inside the parent menu
                if (clickedMenuId === parentMenuId) return;
            }

            onClose();
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen, onClose, ref, menuId, parentMenuId]);

    if (!isOpen) return null;

    return createPortal(
        <div
            className={`fixed bg-(--bg-secondary) rounded-lg shadow-lg border border-gray-200 
                        transition-all duration-200 ${className}
                        ${isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}`}
            style={{
                top: `${pos.top}px`,
                ...(pos.left !== null && { left: `${pos.left}px` }),
                ...(pos.right !== null && { right: `${pos.right}px` }),
                zIndex
            }}
            ref={menuRef}
            role="menu"
            aria-orientation="vertical"
            aria-label={ariaLabel}
            data-menu-id={menuId}
            data-parent-id={parentMenuId}
            data-trigger-id={ref.current?.dataset.triggerId}
        >
            {children}
        </div>,
        document.body
    );
};