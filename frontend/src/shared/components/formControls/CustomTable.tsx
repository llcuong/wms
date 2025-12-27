import { useState, useMemo, ReactNode } from "react";
import { ArrowUpDown, ArrowUp, ArrowDown, Check } from "lucide-react";

export interface TableHeader<T> {
  title: string;
  dataKey: keyof T;
  isSortable?: boolean;
  width?: string;
}

export interface ActionButton<T> {
  icon: ReactNode;
  color?: string;
  onClick: (selectedRows: T[]) => void;
  tooltip?: string;
  disabled?: boolean;
}

export interface TableProps<T> {
  data: T[];
  headers: TableHeader<T>[];
  isCheckbox?: boolean;
  isAutoId?: boolean; // New prop
  actionButtons?: ActionButton<T>[];
  informationElement?: ReactNode;
  onRowClick?: (row: T) => void;
  className?: string;
  width?: string; // New prop
  height?: string; // New prop
  maxWidth?: string;
  maxHeight?: string;
  isDivided?: boolean;
}

// Modern Checkbox Component for reuse
const CustomCheckbox = ({
  checked,
  onChange,
  indeterminate = false,
}: {
  checked: boolean;
  onChange: () => void;
  indeterminate?: boolean;
}) => (
  <div className="relative flex items-center justify-center w-5 h-5 group">
    <input
      type="checkbox"
      className="peer appearance-none w-5 h-5 border-2 border-gray-300 rounded-md checked:bg-indigo-600 checked:border-indigo-600 cursor-pointer transition-all hover:border-indigo-400 focus:ring-2 focus:ring-indigo-200 outline-none"
      checked={checked}
      onChange={onChange}
      onClick={(e) => e.stopPropagation()}
    />
    <Check
      className={`absolute w-3.5 h-3.5 text-white pointer-events-none transition-transform scale-0 peer-checked:scale-100 ${
        indeterminate ? "hidden" : ""
      }`}
      strokeWidth={4}
    />
    {indeterminate && (
      <div className="absolute w-2.5 h-0.5 bg-white pointer-events-none" />
    )}
  </div>
);

export function Table<T extends Record<string, unknown>>({
  data = [],
  headers = [],
  isCheckbox = false,
  isAutoId = false, // Default to false
  actionButtons = [],
  informationElement,
  onRowClick,
  className = "",
  width,
  height,
  maxWidth,
  maxHeight,
  isDivided,
}: TableProps<T>) {
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set());
  const [sortConfig, setSortConfig] = useState<{
    key: keyof T;
    direction: "asc" | "desc";
  } | null>(null);

  // Sorting Logic
  const sortedData = useMemo(() => {
    if (!sortConfig) return data;
    return [...data].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      if (aValue === bValue) return 0;
      if (aValue == null) return 1;
      if (bValue == null) return -1;
      const comparison = aValue < bValue ? -1 : 1;
      return sortConfig.direction === "asc" ? comparison : -comparison;
    });
  }, [data, sortConfig]);

  const handleSort = (dataKey: keyof T) => {
    setSortConfig((current) => {
      if (!current || current.key !== dataKey)
        return { key: dataKey, direction: "asc" };
      if (current.direction === "asc")
        return { key: dataKey, direction: "desc" };
      return null;
    });
  };

  const handleSelectAll = () => {
    if (selectedRows.size === data.length) {
      setSelectedRows(new Set());
    } else {
      setSelectedRows(new Set(data.map((_, index) => index)));
    }
  };

  const handleSelectRow = (index: number) => {
    const newSelected = new Set(selectedRows);
    if (newSelected.has(index)) newSelected.delete(index);
    else newSelected.add(index);
    setSelectedRows(newSelected);
  };

  const getSelectedRowsData = (): T[] =>
    Array.from(selectedRows).map((index) => data[index]);

  const renderSortIcon = (header: TableHeader<T>) => {
    if (!header.isSortable) return null;
    if (!sortConfig || sortConfig.key !== header.dataKey) {
      return (
        <ArrowUpDown className="w-3.5 h-3.5 opacity-40 group-hover:opacity-100 transition-opacity" />
      );
    }
    return sortConfig.direction === "asc" ? (
      <ArrowUp className="w-3.5 h-3.5 text-white" />
    ) : (
      <ArrowDown className="w-3.5 h-3.5 text-white" />
    );
  };

  return (
    <div
      className={`flex flex-col rounded-xl border border-gray-200 bg-white shadow-xl overflow-hidden ${className}`}
      style={{
        width: width,
        height: height,
        maxWidth: maxWidth,
        maxHeight: maxHeight,
      }}
    >
      {/* Scrollable Table Body */}
      <div className="flex-grow overflow-auto scrollbar-thin scrollbar-thumb-gray-300">
        <table className="w-full border-separate border-spacing-0">
          <thead className="sticky top-0 z-20 shadow-sm">
            <tr className="bg-slate-800 text-white">
              {isCheckbox && (
                <th className="px-5 py-4 text-left w-14 bg-slate-800">
                  <CustomCheckbox
                    checked={
                      selectedRows.size === data.length && data.length > 0
                    }
                    onChange={handleSelectAll}
                    indeterminate={
                      selectedRows.size > 0 && selectedRows.size < data.length
                    }
                  />
                </th>
              )}
              {isAutoId && (
                <th className="px-5 py-4 text-left w-16 font-semibold text-xs uppercase tracking-wider bg-slate-800">
                  #
                </th>
              )}
              {headers.map((header, index) => (
                <th
                  key={index}
                  className={`px-5 py-4 text-left group bg-slate-800 transition-colors ${
                    header.isSortable ? "cursor-pointer hover:bg-slate-700" : ""
                  }`}
                  style={{ width: header.width }}
                  onClick={() =>
                    header.isSortable && handleSort(header.dataKey)
                  }
                >
                  <div className="flex items-center gap-2 font-semibold text-xs uppercase tracking-wider">
                    {header.title}
                    {renderSortIcon(header)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white">
            {sortedData.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                onClick={() => onRowClick?.(row)}
                className={`
                  transition-colors group
                  ${selectedRows.has(rowIndex) ? 'bg-indigo-50/50' : 'hover:bg-gray-50'}
                  ${isDivided ? 'border-b border-gray-100' : ''}
                `}
              >
                {/* Manual Border Rendering to bypass divide-y issues */}
                {isCheckbox && (
                  <td className={`px-5 py-3 ${isDivided ? 'border-b border-gray-100' : ''}`}>
                    <CustomCheckbox checked={selectedRows.has(rowIndex)} onChange={() => handleSelectRow(rowIndex)} />
                  </td>
                )}
                {isAutoId && (
                  <td className={`px-5 py-3 text-sm text-gray-400 ${isDivided ? 'border-b border-gray-100' : ''}`}>
                    {rowIndex + 1}
                  </td>
                )}
                {headers.map((h, ci) => (
                  <td 
                    key={ci} 
                    className={`px-5 py-3 text-sm text-gray-700 ${isDivided ? 'border-b border-gray-100' : ''}`}
                  >
                    {String(row[h.dataKey] ?? '-')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Sticky Action Footer */}
      {(actionButtons.length > 0 || informationElement) && (
        <div className="sticky bottom-0 z-20 flex items-center justify-between gap-4 p-4 bg-white border-t border-gray-100 shadow-[0_-4px_12px_rgba(0,0,0,0.03)]">
          <div className="flex items-center gap-3">
            {actionButtons.map((button, index) => (
              <button
                key={index}
                onClick={() => button.onClick(getSelectedRowsData())}
                disabled={button.disabled || selectedRows.size === 0}
                className={`
                  px-4 py-2 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all active:scale-95
                  ${
                    selectedRows.size > 0
                      ? "shadow-md shadow-indigo-100 hover:-translate-y-0.5"
                      : "opacity-40 grayscale pointer-events-none bg-gray-100 text-gray-400"
                  }
                `}
                style={{
                  backgroundColor:
                    selectedRows.size > 0
                      ? button.color || "#4f46e5"
                      : undefined,
                  color: selectedRows.size > 0 ? "white" : undefined,
                }}
              >
                {button.icon}
                {button.tooltip}
              </button>
            ))}
            {selectedRows.size > 0 && (
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-full animate-pulse">
                {selectedRows.size} Selected
              </span>
            )}
          </div>
          {informationElement && (
            <div className="text-sm font-medium text-gray-500 bg-gray-50 px-4 py-2 rounded-lg border border-gray-100">
              {informationElement}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
