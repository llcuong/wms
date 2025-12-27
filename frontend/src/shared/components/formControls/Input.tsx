import React, { useEffect, useRef } from 'react';
import { BaseControlProps } from './types';

interface InputProps extends BaseControlProps {
  value?: string;
  onChange: (value: string) => void;
  type?: 'text' | 'number' | 'email' | 'password';
}

export const Input: React.FC<InputProps> = ({
  label,
  placeholder = '',
  value = '',
  onChange,
  disabled = false,
  required = false,
  error = '',
  type = 'text',
  className = '',
  isFocus = false
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isFocus && !disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isFocus, disabled]);

  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <input
        ref={inputRef}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className={`
          px-3 py-2 rounded-lg border transition-all duration-200
          ${disabled 
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-200' 
            : 'bg-white text-gray-900 border-gray-300 hover:border-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100'
          }
          ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-100' : ''}
          outline-none text-sm
        `}
      />
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};