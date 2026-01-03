import { createPortal } from "react-dom";
import React, { useEffect, useRef, useState } from "react";

import { useSlots } from "./useSlots";
import { createSlot } from "../Navbar/createSlots";

interface Position {
    top: number;
    left: number | null;
    right: number | null;
};

interface DropdownCustomProps {
    triggerRef: React.RefObject<HTMLElement>;
    isOpen: boolean;
    onClose: () => void;
    children: React.ReactNode;
    className: string;
    align: "right" | "left";
    menuId: string;
    ariaLabel: string;
    parentMenuId: string | null;
    offset?: number;
    zIndex?: number;
};

export const DropdownCustom = Object.assign(
    ({
        triggerRef,
        isOpen,
        onClose,
        children,
        className = '',
        offset = 30,
        align = 'left',
        menuId = `menu-${Math.random().toString(36).substring(2, 9)}`,
        parentMenuId = null,
        ariaLabel,
        zIndex = 30,
    }: DropdownCustomProps) => {
        const { header, body, footer } = useSlots(children);

        const menuRef = useRef<HTMLDivElement>(null);

        const [position, setPosition] = useState<Position>({ top: 0, left: null, right: null });
        const [isVisible, setIsVisible] = useState(false);

        useEffect(() => {
            if (triggerRef.current && !triggerRef.current.dataset.triggerId)
                triggerRef.current.dataset.triggerId = menuId;
        }, [triggerRef, menuId]);

        // Calculate and update menu position
        useEffect(() => {
            if (!isOpen) return;

            const updatePosition = () => {
                if (triggerRef.current) {
                    const rect = triggerRef.current.getBoundingClientRect();
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

                    setPosition(positionStyle);
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
        }, [triggerRef, isOpen, offset, align]);

        // Close menu when clicking outside
        useEffect(() => {
            if (!isOpen) return;

            const handleClickOutside = (event: MouseEvent) => {
                const target = event.target as HTMLElement;

                if (menuRef.current?.contains(target)) return;
                if (triggerRef.current?.contains(target)) return;

                const clickedMenu = target.closest<HTMLElement>('[role="menu"]');
                if (clickedMenu) {
                    const clickedParentId = clickedMenu.dataset.parentId;
                    const clickedMenuId = clickedMenu.dataset.menuId;

                    if (clickedParentId === menuId) return;
                    if (clickedMenuId === parentMenuId) return;
                }

                onClose();
            };

            document.addEventListener("mousedown", handleClickOutside);
            return () => document.removeEventListener("mousedown", handleClickOutside);
        }, [isOpen, onClose, triggerRef, menuId, parentMenuId]);

        return createPortal(
            <div
                className={`fixed bg-white rounded-lg shadow-lg border border-gray-200 ${className}
                            flex flex-col items-start justify-center gap-4
                            ${isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95'}`}
                style={{
                    top: `${position.top}px`,
                    ...(position.left !== null && { left: `${position.left}px` }),
                    ...(position.right !== null && { right: `${position.right}px` }),
                    zIndex
                }}
                ref={menuRef}
                role="menu"
                aria-orientation="vertical"
                aria-label={ariaLabel}
                data-menu-id={menuId}
                data-parent-id={parentMenuId}
                data-trigger-id={triggerRef.current?.dataset.triggerId}
            >
                <div className="flex-none mx-4 min-w-0">{header}</div>
                <div className="flex-none mx-4 min-w-0">{body}</div>
                <div className="flex-none mx-4 min-w-0">{footer}</div>
            </div>,
            document.body
        );
    },
    {
        Header: createSlot("Dropdown.Header"),
        Body: createSlot("Dropdown.Body"),
        Footer: createSlot("Dropdown.Footer"),
    }
);