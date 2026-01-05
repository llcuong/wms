import React, { Dispatch } from "react";
import { useTranslation } from "react-i18next";

import useAddAccount from "./useAddAccount";

interface FormInputProps {
    type?: 'text' | 'password';
    labelText: string;
    labelKey: string;
    required?: boolean;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder?: string;
};

const FormInput = ({ type, labelText, labelKey, required, value, onChange, placeholder }: FormInputProps) => (
    <div key={labelKey}>
        <label htmlFor={labelKey} className="block text-sm font-medium text-(--text-primary) mb-1">
            {labelText} {required && <span className="text-red-500">*</span>}
        </label>
        <input type={type} id={labelKey} name={labelKey} placeholder={placeholder}
            required={required}
            value={value}
            onChange={onChange}
            className="w-full px-4 py-2.5 border border-(--color-secondary) rounded-xl focus:outline-none text-(--text-primary)
                        focus:ring-1 focus:ring-(--color-primary) focus:border-transparent transition-colors duration-300"
        />
    </div>
);

interface FormButtonProps {
    type: "button" | "submit" | "reset";
    className: string;
    disabled?: boolean;
    label: string;
    onClick: (e: React.FormEvent) => void;
};

const FormButton = ({ type, className, disabled, label, onClick }: FormButtonProps) => (
    <button type={type} onClick={onClick} disabled={disabled}
        className={`px-5 py-2.5 rounded-xl transition-colors duration-300 cursor-pointer font-medium ${className}`}
    >
        {label}
    </button>
);

interface AddAccountModalProps {
    isOpen: boolean;
    setIsOpen: Dispatch<React.SetStateAction<boolean>>;
    userId: string;
    setUserId: Dispatch<React.SetStateAction<string>>;
    getUserList: () => Promise<void>;
};

export default function CreateAccountModal({ isOpen, setIsOpen, userId, setUserId, getUserList }: AddAccountModalProps) {
    const { t } = useTranslation();

    const {
        formData,
        isLoading,
        handleChange,
        handleSubmit,
    } = useAddAccount({ userId, setIsOpen, setUserId, getUserList });

    const FORM_INPUT_LIST: FormInputProps[] = [
        {
            type: "text",
            labelText: t("label.accountId"),
            labelKey: "account_id",
            required: true,
            value: formData.account_id,
            onChange: handleChange,
            placeholder: "e.g., john.doe",
        },
        {
            type: "password",
            labelText: t("label.password"),
            labelKey: "password",
            required: true,
            value: formData.password,
            onChange: handleChange,
            placeholder: t("placeholder.enterPassword"),
        },
    ];

    const FORM_BUTTON_LIST: FormButtonProps[] = [
        {
            type: "button",
            className: "bg-gray-200 text-gray-800 hover:bg-gray-400",
            disabled: false,
            label: t("button.cancel"),
            onClick: () => setIsOpen(false),
        },
        {
            type: "submit",
            className: "bg-green-600 text-white hover:bg-green-800 disabled:opacity-50",
            disabled: isLoading,
            label: isLoading ? t("status.adding") : t("button.addAccount"),
            onClick: handleSubmit,
        },
    ];

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
            <div className="bg-(--bg-secondary) rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
                <div className="bg-(--color-primary) px-6 py-4">
                    <h2 className="text-xl font-bold text-(--bg-primary)">{t("title.addAccount")}</h2>
                    <p className="text-(--bg-primary) text-sm mt-1">{t("description.addAccount", { userId })}</p>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    {FORM_INPUT_LIST.map((input) => (
                        <FormInput
                            key={input.labelKey}
                            type={input.type}
                            labelText={input.labelText}
                            labelKey={input.labelKey}
                            required={input.required}
                            value={input.value}
                            onChange={input.onChange}
                            placeholder={input.placeholder}
                        />
                    ))}

                    <div className="flex justify-end gap-3 pt-4">
                        {FORM_BUTTON_LIST.map((button, index) => (
                            <FormButton key={index}
                                type={button.type}
                                className={button.className}
                                label={button.label}
                                onClick={button.onClick}
                            />
                        ))}
                    </div>
                </form>
            </div>
        </div>
    );
};