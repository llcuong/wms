import { useState, useCallback, ReactNode } from "react";
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from "lucide-react";
import { ToastContext } from "@components/toast/toastContext";
import type { Toast, ToastType } from "./toast.types";
import { nanoid } from "nanoid";

interface Props {
  children: ReactNode;
}

export const ToastProvider = ({ children }: Props) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) =>
      prev.map((t) => (t.id === id ? { ...t, closing: true } : t))
    );

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 250);
  }, []);

  const addToast = useCallback(
    (message: string, type: ToastType = "info", duration = 3000) => {
      const id = nanoid();
      setToasts((prev) => [...prev, { id, message, type }]);

      if (duration > 0) {
        setTimeout(() => removeToast(id), duration);
      }
    },
    [removeToast]
  );

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}

      <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-center gap-3 min-w-[300px] p-4 rounded-lg shadow-lg border-l-4 bg-white ${toast.closing ? "animate-slide-out" : "animate-slide-in"}
              ${
                toast.type === "success"
                  ? "border-green-500"
                  : toast.type === "error"
                  ? "border-red-500"
                  : toast.type === "warning"
                  ? "border-yellow-500"
                  : "border-blue-500"
              }`}
          >
            {toast.type === "success" && (
              <CheckCircle className="text-green-500" />
            )}
            {toast.type === "error" && <AlertCircle className="text-red-500" />}
            {toast.type === "warning" && (
              <AlertTriangle className="text-yellow-500" />
            )}
            {toast.type === "info" && <Info className="text-blue-500" />}

            <p className="flex-grow text-sm font-medium">{toast.message}</p>

            <button onClick={() => removeToast(toast.id)}>
              <X size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};
