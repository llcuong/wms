import React, { useState, useRef, useEffect, JSX } from "react";
import { Calendar } from "lucide-react";
import { BaseControlProps } from "./types";

interface DatePickerProps extends BaseControlProps {
  value?: string;
  onChange: (value: string) => void;
  type?: "day" | "month" | "year";
}

export const DatePicker: React.FC<DatePickerProps> = ({
  label,
  placeholder,
  value = "",
  onChange,
  disabled = false,
  required = false,
  type = "day",
  error = "",
  className = "",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [viewDate, setViewDate] = useState(new Date());
  const pickerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        pickerRef.current &&
        !pickerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const formatPlaceholder = () => {
    if (placeholder) return placeholder;
    if (type === "day") return "mm/dd/yyyy";
    if (type === "month") return "mm/yyyy";
    return "yyyy";
  };

  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    return { firstDay, daysInMonth };
  };

  const handleDateSelect = (day: number) => {
    const date = new Date(viewDate.getFullYear(), viewDate.getMonth(), day);
    onChange(date.toLocaleDateString("en-US"));
    setIsOpen(false);
  };

  const handleMonthSelect = (month: number) => {
    const date = new Date(viewDate.getFullYear(), month, 1);
    onChange(`${String(month + 1).padStart(2, "0")}/${date.getFullYear()}`);
    setIsOpen(false);
  };

  const handleYearSelect = (year: number) => {
    onChange(String(year));
    setIsOpen(false);
  };

  const renderDayPicker = () => {
    const { firstDay, daysInMonth } = getDaysInMonth(viewDate);
    const days: JSX.Element[] = [];

    for (let i = 0; i < firstDay; i++) {
      days.push(<div key={`empty-${i}`} className="p-2" />);
    }

    for (let day = 1; day <= daysInMonth; day++) {
      days.push(
        <button
          key={day}
          onClick={() => handleDateSelect(day)}
          className="p-2 hover:bg-blue-50 rounded transition-colors text-sm"
        >
          {day}
        </button>
      );
    }

    return days;
  };

  const renderMonthPicker = () => {
    const months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    return months.map((month, idx) => (
      <button
        key={idx}
        onClick={() => handleMonthSelect(idx)}
        className="p-3 hover:bg-blue-50 rounded transition-colors text-sm"
      >
        {month}
      </button>
    ));
  };

  const renderYearPicker = () => {
    const currentYear = new Date().getFullYear();
    const years: JSX.Element[] = [];
    for (let i = currentYear - 10; i <= currentYear + 10; i++) {
      years.push(
        <button
          key={i}
          onClick={() => handleYearSelect(i)}
          className="p-3 hover:bg-blue-50 rounded transition-colors text-sm"
        >
          {i}
        </button>
      );
    }
    return years;
  };

  return (
    <div className={`flex flex-col gap-1.5 ${className}`} ref={pickerRef}>
      {label && (
        <label className="text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <div className="relative">
        <div
          onClick={() => !disabled && setIsOpen(!isOpen)}
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
          <span className={value ? "text-gray-900" : "text-gray-400"}>
            {value || formatPlaceholder()}
          </span>
          <Calendar className="w-4 h-4 text-gray-400" />
        </div>

        {isOpen && !disabled && (
          <div className="absolute z-50 w-full min-w-100 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg p-4">
            {type === "day" && (
              <>
                <div className="flex items-center justify-between mb-3">
                  <button
                    onClick={() =>
                      setViewDate(
                        new Date(
                          viewDate.getFullYear(),
                          viewDate.getMonth() - 1
                        )
                      )
                    }
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    ←
                  </button>
                  <span className="font-medium text-sm">
                    {viewDate.toLocaleDateString("en-US", {
                      month: "long",
                      year: "numeric",
                    })}
                  </span>
                  <button
                    onClick={() =>
                      setViewDate(
                        new Date(
                          viewDate.getFullYear(),
                          viewDate.getMonth() + 1
                        )
                      )
                    }
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    →
                  </button>
                </div>
                <div className="grid grid-cols-7 gap-1">
                  {["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"].map((day) => (
                    <div
                      key={day}
                      className="text-center text-xs font-medium text-gray-500 p-2"
                    >
                      {day}
                    </div>
                  ))}
                  {renderDayPicker()}
                </div>
              </>
            )}

            {type === "month" && (
              <>
                <div className="flex items-center justify-between mb-3">
                  <button
                    onClick={() =>
                      setViewDate(new Date(viewDate.getFullYear() - 1, 0))
                    }
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    ←
                  </button>
                  <span className="font-medium text-sm">
                    {viewDate.getFullYear()}
                  </span>
                  <button
                    onClick={() =>
                      setViewDate(new Date(viewDate.getFullYear() + 1, 0))
                    }
                    className="p-1 hover:bg-gray-100 rounded"
                  >
                    →
                  </button>
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {renderMonthPicker()}
                </div>
              </>
            )}

            {type === "year" && (
              <div className="grid grid-cols-3 gap-2 max-h-60 overflow-auto">
                {renderYearPicker()}
              </div>
            )}
          </div>
        )}
      </div>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
};
