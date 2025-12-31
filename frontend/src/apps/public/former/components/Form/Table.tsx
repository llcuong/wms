import { useState, useMemo, ReactNode, useEffect } from "react";
import {
  ArrowUpDown,
  ArrowUp,
  ArrowDown,
  Check,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
} from "lucide-react";

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

export interface PaginationConfig {
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
  paginationInfo?: boolean;
  onPageChange: (page: number) => void;
  onItemsPerPageChange?: (itemsPerPage: number) => void;
  itemsPerPageOptions?: number[];
}

export interface TableProps<T> {
  data: T[];
  fullData?: T[];
  rowKey: keyof T | ((row: T) => string);
  headers: TableHeader<T>[];
  isCheckbox?: boolean;
  isAutoId?: boolean;
  actionButtons?: ActionButton<T>[];
  informationElement?: ReactNode;
  onSelectionChange?: (selectedRows: T[]) => void;
  onRowClick?: (row: T) => void;
  className?: string;
  width?: string;
  height?: string;
  maxWidth?: string;
  maxHeight?: string;
  isDivided?: boolean;
  pagination?: PaginationConfig;
}

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

const Pagination = ({ config }: { config: PaginationConfig }) => {
  const {
    currentPage,
    itemsPerPage,
    totalItems,
    paginationInfo = false,
    onPageChange,
    onItemsPerPageChange,
    itemsPerPageOptions = [10, 25, 50, 100],
  } = config;

  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  // Generate page numbers to display
  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    const maxVisible = 7;

    if (totalPages <= maxVisible) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    // Always show first page
    pages.push(1);

    if (currentPage > 3) {
      pages.push("...");
    }

    // Show pages around current page
    const start = Math.max(2, currentPage - 1);
    const end = Math.min(totalPages - 1, currentPage + 1);

    for (let i = start; i <= end; i++) {
      pages.push(i);
    }

    if (currentPage < totalPages - 2) {
      pages.push("...");
    }

    if (totalPages > 1) {
      pages.push(totalPages);
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex items-center justify-between gap-4 flex-wrap">
      {onItemsPerPageChange && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Show</span>
          <select
            value={itemsPerPage}
            onChange={(e) => onItemsPerPageChange(Number(e.target.value))}
            className="px-3 py-1.5 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
          >
            {itemsPerPageOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
          <span className="text-sm text-gray-600">per page</span>
        </div>
      )}

      {paginationInfo && (
        <div className="text-sm text-gray-600 font-medium">
          Showing <span className="text-indigo-600">{startItem}</span> to{" "}
          <span className="text-indigo-600">{endItem}</span> of{" "}
          <span className="text-indigo-600">{totalItems}</span> results
        </div>
      )}

      <div className="flex items-center gap-1">
        <button
          onClick={() => onPageChange(1)}
          disabled={currentPage === 1}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          title="First page"
        >
          <ChevronsLeft className="w-4 h-4" />
        </button>

        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          title="Previous page"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-1">
          {pageNumbers.map((page, index) => {
            if (page === "...") {
              return (
                <span key={`ellipsis-${index}`} className="px-2 text-gray-400">
                  ...
                </span>
              );
            }

            return (
              <button
                key={page}
                onClick={() => onPageChange(page as number)}
                className={`
                                  min-w-[2.5rem] px-3 py-1.5 rounded-lg font-medium text-sm transition-all
                                  ${
                                    currentPage === page
                                      ? "bg-indigo-600 text-white shadow-md"
                                      : "hover:bg-gray-100 text-gray-700"
                                  }
                `}
              >
                {page}
              </button>
            );
          })}
        </div>

        {/* Next page */}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          title="Next page"
        >
          <ChevronRight className="w-4 h-4" />
        </button>

        {/* Last page */}
        <button
          onClick={() => onPageChange(totalPages)}
          disabled={currentPage === totalPages}
          className="p-2 rounded-lg hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          title="Last page"
        >
          <ChevronsRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export function Table<T extends Record<string, unknown>>({
  data = [],
  rowKey,
  fullData,
  headers = [],
  isCheckbox = false,
  isAutoId = false,
  actionButtons = [],
  informationElement,
  onSelectionChange,
  onRowClick,
  className = "",
  width,
  height,
  maxWidth,
  maxHeight,
  isDivided,
  pagination,
}: TableProps<T>) {
  const [selectedRows, setSelectedRows] = useState<Set<string>>(new Set());
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

  const getRowId = (row: T): string => {
    return typeof rowKey === "function" ? rowKey(row) : String(row[rowKey]);
  };

  const handleSort = (dataKey: keyof T) => {
    setSortConfig((current) => {
      if (!current || current.key !== dataKey)
        return { key: dataKey, direction: "asc" };
      if (current.direction === "asc")
        return { key: dataKey, direction: "desc" };
      return null;
    });
  };

  const notifySelectionChange = (nextSelected: Set<string>) => {
    setSelectedRows(nextSelected);

    if (onSelectionChange) {
      const source = fullData ?? data;
      const selectedData = source.filter((row) =>
        nextSelected.has(getRowId(row))
      );
      onSelectionChange(selectedData);
    }
  };

  const pageRowIds = sortedData.map(getRowId);

  // const handleSelectAll = () => {
  //   const allSelected = pageRowIds.every((id) => selectedRows.has(id));

  //   const newSelected = new Set(selectedRows);

  //   if (allSelected) {
  //     pageRowIds.forEach((id) => newSelected.delete(id));
  //   } else {
  //     pageRowIds.forEach((id) => newSelected.add(id));
  //   }

  //   setSelectedRows(newSelected);
  // };

  const handleSelectAll = () => {
    const source = fullData ?? data;
    const allRowIds = source.map(getRowId);

    const allSelected = allRowIds.every((id) => selectedRows.has(id));

    if (allSelected) {
      notifySelectionChange(new Set());
    } else {
      notifySelectionChange(new Set(allRowIds));
    }
  };

  const handleSelectRow = (row: T) => {
    const id = getRowId(row);
    const newSelected = new Set(selectedRows);

    if (newSelected.has(id)) newSelected.delete(id);
    else newSelected.add(id);

    notifySelectionChange(newSelected);
  };

  useEffect(() => {
    setTimeout(() => {
      notifySelectionChange(new Set());
    }, 0);
  }, [fullData]);

  const getSelectedRowsData = (): T[] => {
    const source = fullData ?? data;
    return source.filter((row) => selectedRows.has(getRowId(row)));
  };

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

  const getRowNumber = (rowIndex: number) => {
    if (pagination) {
      return (
        (pagination.currentPage - 1) * pagination.itemsPerPage + rowIndex + 1
      );
    }
    return rowIndex + 1;
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
                      pageRowIds.length > 0 &&
                      pageRowIds.every((id) => selectedRows.has(id))
                    }
                    indeterminate={
                      pageRowIds.some((id) => selectedRows.has(id)) &&
                      !pageRowIds.every((id) => selectedRows.has(id))
                    }
                    onChange={handleSelectAll}
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
            {sortedData.length === 0 ? (
              <tr>
                <td
                  colSpan={
                    headers.length + (isCheckbox ? 1 : 0) + (isAutoId ? 1 : 0)
                  }
                  className="px-5 py-12 text-center text-gray-400"
                >
                  <div className="flex flex-col items-center gap-2">
                    <svg
                      className="w-12 h-12 text-gray-300"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                      />
                    </svg>
                    <span className="text-sm font-medium">
                      No data available
                    </span>
                  </div>
                </td>
              </tr>
            ) : (
              sortedData.map((row, rowIndex) => {
                const rowId = getRowId(row);

                return (
                  <tr
                    key={rowId}
                    onClick={() => onRowClick?.(row)}
                    className={`
                    transition-colors group
                    ${
                      selectedRows.has(rowId)
                        ? "bg-indigo-50/50"
                        : "hover:bg-gray-50"
                    }
                    ${isDivided ? "border-b border-gray-100" : ""}
                  `}
                  >
                    {isCheckbox && (
                      <td
                        className={`px-5 py-3 ${
                          isDivided ? "border-b border-gray-100" : ""
                        }`}
                      >
                        <CustomCheckbox
                          checked={selectedRows.has(getRowId(row))}
                          onChange={() => handleSelectRow(row)}
                        />
                      </td>
                    )}
                    {isAutoId && (
                      <td
                        className={`px-5 py-3 text-sm text-gray-400 font-medium ${
                          isDivided ? "border-b border-gray-100" : ""
                        }`}
                      >
                        {getRowNumber(rowIndex)}
                      </td>
                    )}
                    {headers.map((h, ci) => (
                      <td
                        key={ci}
                        className={`px-5 py-3 text-sm text-gray-700 ${
                          isDivided ? "border-b border-gray-100" : ""
                        }`}
                      >
                        {String(row[h.dataKey] ?? "-")}
                      </td>
                    ))}
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Sticky Action Footer */}
      {(actionButtons.length > 0 || informationElement || pagination) && (
        <div className="sticky bottom-0 z-20 bg-white border-t border-gray-200 shadow-[0_-4px_12px_rgba(0,0,0,0.03)]">
          {/* Action buttons and info */}
          <div className="flex items-center justify-between gap-4 p-4 border-b border-gray-100">
            {actionButtons.length > 0 && (
              <div className="flex items-center gap-3">
                {actionButtons.map((button, index) => (
                  <button
                    key={index}
                    onClick={() => button.onClick(getSelectedRowsData())}
                    disabled={button.disabled || selectedRows.size === 0}
                    className={`
                      px-4 py-2 rounded-lg font-semibold text-sm flex items-center gap-2 transition-all active:scale-95 cursor-pointer
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
            )}

            {pagination && <Pagination config={pagination} />}
            {informationElement && (
              <div className="text-sm font-medium text-gray-500 bg-gray-50 px-4 py-2 rounded-lg border border-gray-100">
                {informationElement}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
