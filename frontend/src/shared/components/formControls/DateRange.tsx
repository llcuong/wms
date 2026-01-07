import React from 'react';
import { DatePicker } from './DatePicker';
import { BaseControlProps } from './types';

interface DateRangeProps extends BaseControlProps {
  start?: string;
  end?: string;
  onChange: (start: string, end: string) => void;
  type?: 'day' | 'month' | 'year';
}

export const DateRange: React.FC<DateRangeProps> = ({
  label,
  start = '',
  end = '',
  onChange,
  type = 'day',
  disabled = false,
  required = false,
  error = '',
  className = ''
}) => {
  return (
    <div className={`flex flex-col gap-1.5 ${className}`}>
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}

      <div className="flex gap-2">
        <DatePicker
          value={start}
          type={type}
          onChange={(v) => onChange(v, end)}
          disabled={disabled}
          placeholder="Start date"
        />
        <DatePicker
          value={end}
          type={type}
          onChange={(v) => onChange(start, v)}
          disabled={disabled}
          placeholder="End date"
        />
      </div>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};