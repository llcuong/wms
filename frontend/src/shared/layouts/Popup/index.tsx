import React, { useEffect, useRef } from "react";
import { createPortal } from "react-dom";

import { useSlots } from "./useSlots";
import { createSlot } from "../Navbar/createSlots";

interface PopupProps {
    isOpen: boolean;
    onClose: () => void;
    children: React.ReactNode;
};

export const Popup = Object.assign(
    ({
        isOpen,
        onClose,
        children
    }: PopupProps) => {
        const { header, body, footer } = useSlots(children);

        const popupRef = useRef<HTMLDivElement>(null);

        useEffect(() => {
            if (!isOpen) return;

            const handleClickOutside = (event: MouseEvent) => {
                if (!(event.target instanceof Node)) return;
                if (popupRef.current && !popupRef.current.contains(event.target)) {
                    onClose();
                }
            };

            document.addEventListener("mousedown", handleClickOutside);

            return () => {
                document.removeEventListener("mousedown", handleClickOutside);
            };
        }, [isOpen, onClose]);

        if (!isOpen) return null;

        return createPortal(
            <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 animate-fadeIn">
                <div
                    ref={popupRef}
                    className="bg-white w-full max-w-md rounded-2xl p-6 shadow-xl animate-scaleIn relative
                                flex flex-col items-start justify-center gap-4"
                >
                    <div className="flex-none mx-4 min-w-0">{header}</div>
                    <div className="flex-none mx-4 min-w-0">{body}</div>
                    <div className="flex-none mx-4 min-w-0">{footer}</div>
                </div>
            </div>,
            document.body
        );
    },
    {
        Header: createSlot("Popup.Header"),
        Body: createSlot("Popup.Body"),
        Footer: createSlot("Popup.Footer"),
    }
);