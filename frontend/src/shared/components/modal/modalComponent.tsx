import React, { useEffect, useRef } from "react";
import {
  X,
  CheckCircle,
  AlertCircle,
  AlertTriangle,
  Info,
  HelpCircle,
} from "lucide-react";
import { ModalType } from "@components/modal/modal.types";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children?: React.ReactNode;
  type?: ModalType;
  // Actions
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
  isLoading?: boolean;
  width?: string;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  type = "default",
  onConfirm,
  confirmText = "Confirm",
  cancelText = "Cancel",
  isLoading = false,
  width = "max-w-md", // Default width, can be overridden (e.g., 'max-w-2xl')
}) => {
  const modalRef = useRef<HTMLDivElement>(null);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  // Click outside to close
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (modalRef.current && !modalRef.current.contains(e.target as Node)) {
      onClose();
    }
  };

  // Close after process onConfirm
  const handleConfirm = async () => {
    if (!onConfirm) return;

    try {
      await onConfirm();
    } finally {
      onClose();
    }
  };

  if (!isOpen) return null;

  // Configuration for different types (Colors & Icons)
  const config = {
    success: {
      icon: CheckCircle,
      color: "text-green-600",
      bg: "bg-green-100",
      btn: "bg-green-600 hover:bg-green-700",
    },
    error: {
      icon: AlertCircle,
      color: "text-red-600",
      bg: "bg-red-100",
      btn: "bg-red-600 hover:bg-red-700",
    },
    warning: {
      icon: AlertTriangle,
      color: "text-yellow-600",
      bg: "bg-yellow-100",
      btn: "bg-yellow-600 hover:bg-yellow-700",
    },
    info: {
      icon: Info,
      color: "text-blue-600",
      bg: "bg-blue-100",
      btn: "bg-blue-600 hover:bg-blue-700",
    },
    confirm: {
      icon: HelpCircle,
      color: "text-indigo-600",
      bg: "bg-indigo-100",
      btn: "bg-indigo-600 hover:bg-indigo-700",
    },
    default: {
      icon: null,
      color: "text-gray-900",
      bg: "bg-gray-100",
      btn: "bg-gray-900 hover:bg-gray-800",
    },
  };

  const currentConfig = config[type];
  const Icon = currentConfig.icon;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 backdrop-blur-sm transition-opacity animate-fade-in p-4"
      onClick={handleBackdropClick}
    >
      <div
        ref={modalRef}
        className={`bg-white rounded-xl shadow-2xl w-full ${width} transform transition-all animate-scale-in flex flex-col max-h-[90vh]`}
      >
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {Icon && (
              <div className={`p-2 rounded-full ${currentConfig.bg}`}>
                <Icon className={`w-5 h-5 ${currentConfig.color}`} />
              </div>
            )}
            <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors text-gray-400 hover:text-gray-600"
          >
            <X size={20} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto">
          {children ? (
            children
          ) : (
            <p className="text-gray-600">Are you sure you want to proceed?</p>
          )}
        </div>

        {/* Footer (Only if type is NOT default or if onConfirm is passed) */}
        {(type !== "default" || onConfirm) && (
          <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-end gap-3 rounded-b-xl">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-200"
            >
              {cancelText}
            </button>
            {onConfirm && (
              <button
                onClick={handleConfirm}
                disabled={isLoading}
                className={`px-4 py-2 text-sm font-medium text-white rounded-lg shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 ${currentConfig.btn} disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2`}
              >
                {isLoading && (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                )}
                {confirmText}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
