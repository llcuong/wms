import React, { useState, useRef, useEffect } from "react";
import { ChevronDown, X, Check, Search } from "lucide-react";
import { BaseControlProps, DropdownOption, DropdownAction } from "./types";

interface DropdownProps extends BaseControlProps {
  value?: string;
  onChange: (value: string) => void;
  options: DropdownOption[];
  isSearch?: boolean;
  isTyping?: boolean;
  exFunctions?: DropdownAction[];
}

export const Dropdown: React.FC<DropdownProps> = ({
  label,
  placeholder = "Select or typing...",
  value = "",
  onChange,
  options = [],
  disabled = false,
  required = false,
  isSearch = false,
  isTyping = false,
  exFunctions = [],
  error = "",
  className = "",
  isFocus = false,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);

  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!isFocus || disabled) return;

    setTimeout(() => {
      setIsOpen(true);
    }, 0);

    if (isTyping && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isFocus, disabled, isTyping]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
        setSearchTerm("");
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Helper to find the label associated with a value
  const getLabelFromValue = (val: string) => {
    const option = options.find((opt) => opt.value === val);
    return option ? option.label : val;
  };

  // Filter logic:
  const filteredOptions = options.filter((option) => {
    const searchTarget = isTyping ? getLabelFromValue(value) : searchTerm;
    return option.label.toLowerCase().includes(searchTarget.toLowerCase());
  });

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    onChange("");
    setSearchTerm("");
  };

  return (
    <div className={`flex flex-col gap-1.5 ${className}`} ref={dropdownRef}>
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        <div
          onClick={() => !disabled && setIsOpen(true)}
          className={`
            px-3 py-2 rounded-lg border transition-all duration-200 flex items-center justify-between gap-2
            ${
              disabled
                ? "bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200"
                : "bg-white text-gray-900 border-gray-300 hover:border-gray-400 cursor-pointer"
            }
            ${error ? "border-red-500" : ""}
            ${isOpen && !disabled ? "border-blue-500 ring-2 ring-blue-100" : ""}
            outline-none text-sm
          `}
        >
          {isTyping ? (
            <input
              ref={inputRef}
              type="text"
              value={getLabelFromValue(value)}
              onChange={(e) => {
                onChange(e.target.value);
                setIsOpen(true);
              }}
              placeholder={placeholder}
              disabled={disabled}
              className="flex-1 outline-none bg-transparent cursor-text"
              onClick={(e) => {
                e.stopPropagation();
                setIsOpen(true);
              }}
            />
          ) : (
            <span
              tabIndex={disabled ? -1 : 0}
              className={`flex-1 ${value ? "text-gray-900" : "text-gray-400"}`}
            >
              {getLabelFromValue(value) || placeholder}
            </span>
          )}

          <div className="flex items-center gap-1">
            {exFunctions.map((func, idx) => (
              <button
                key={idx}
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  func.onClick();
                }}
                disabled={disabled}
                className="p-1 hover:bg-gray-100 rounded transition-colors disabled:opacity-50 cursor-pointer"
              >
                {func.icon}
              </button>
            ))}
            {value && !disabled && (
              <button
                type="button"
                onClick={handleClear}
                className="p-1 hover:bg-gray-100 rounded transition-colors cursor-pointer"
              >
                <X className="w-4 h-4 text-gray-400" />
              </button>
            )}
            <ChevronDown
              className={`w-4 h-4 text-gray-400 transition-transform cursor-pointer ${
                isOpen ? "rotate-180" : ""
              }`}
              onClick={(e: React.MouseEvent) => {
                if (!disabled) {
                  e.stopPropagation();
                  setIsOpen(!isOpen);
                }
              }}
            />
          </div>
        </div>

        {isOpen && !disabled && (
          <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg overflow-hidden flex flex-col">
            {isSearch && !isTyping && (
              <div className="p-2 border-b border-gray-100 bg-gray-50 flex items-center gap-2">
                <Search className="w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  autoFocus
                  placeholder="Search..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full bg-transparent text-sm outline-none"
                  onClick={(e) => e.stopPropagation()}
                />
              </div>
            )}

            <div className="overflow-auto max-h-60">
              {filteredOptions.length > 0 ? (
                filteredOptions.map((option, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      onChange(option.value); // Sends the VALUE to the parent
                      setIsOpen(false);
                      setSearchTerm("");
                    }}
                    className={`
                      px-3 py-2 cursor-pointer transition-colors text-sm flex items-center justify-between
                      ${
                        value === option.value
                          ? "bg-blue-50 text-blue-600 font-medium"
                          : "text-gray-700 hover:bg-gray-50"
                      }
                    `}
                  >
                    <span>{option.label}</span>
                    {value === option.value && <Check className="w-4 h-4" />}
                  </div>
                ))
              ) : (
                <div className="px-3 py-4 text-sm text-gray-400 text-center italic">
                  No matching options
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      {error && <span className="text-xs text-red-500 mt-1">{error}</span>}
    </div>
  );
};
