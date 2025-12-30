import { useState, useEffect } from "react";
import { Base } from "../Base";
import type { PageNavigatorComponent } from "@routes/types";
import { Input } from "@components/formControls/Input";
import { DatePicker } from "@components/formControls/DatePicker";
import { Dropdown } from "@components/formControls/Dropdown";
import { PlusCircle, FileDown, Printer, Trash2 } from "lucide-react";
import {
  PaginationConfig,
  Table,
  TableHeader,
  ActionButton,
} from "@components/formControls/CustomTable";
import { useToast } from "@components/toast";
import { useModal } from "@components/modal";

interface BasketData {
  [key: string]: unknown;
  basket_no: string;
  brand: string;
  capacity: string;
  length: string;
  received_date: string;
  purchase_order: string;
  create_group: string;
}

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debouncedValue;
}

const AddBasketPage: PageNavigatorComponent = (props) => {
  // --- Toast ---
  const { addToast } = useToast();

  // --- Modal ---
  const { showModal } = useModal();

  // --- Form States ---
  const [purchaseOrder, setPurchaseOrder] = useState("");
  const [brand, setBrand] = useState<string | undefined>(undefined);
  const [receiveQty, setReceiveQty] = useState("");
  const [basketWidth, setBasketWidth] = useState<string | undefined>(undefined);
  const [receiveDate, setReceiveDate] = useState("2025-12-26");
  const [capacity, setCapacity] = useState("5");
  const [plantCode, setPlantCode] = useState<string | undefined>(undefined);
  const [note, setNote] = useState("");

  const [focusField, setFocusField] = useState<
    "po" | "brand" | "qty" | "width" | "plant" | "note"
  >("po");

  const debouncedQty = useDebounce(receiveQty, 1000);

  useEffect(() => {
    if (purchaseOrder.length === 10 && !brand) {
      const timeoutId = setTimeout(() => {
        setFocusField("brand");
      }, 0);

      return () => clearTimeout(timeoutId);
    }

    if (brand && !receiveQty) {
      const timeoutId = setTimeout(() => {
        setFocusField("qty");
      }, 0);
      return () => clearTimeout(timeoutId);
    }

    if (receiveQty && !basketWidth && debouncedQty) {
      const timeoutId = setTimeout(() => {
        setFocusField("width");
      }, 0);
      return () => clearTimeout(timeoutId);
    }

    if (basketWidth && !plantCode) {
      const timeoutId = setTimeout(() => {
        setFocusField("plant");
      }, 0);
      return () => clearTimeout(timeoutId);
    }

    if (plantCode && !note) {
      const timeoutId = setTimeout(() => {
        setFocusField("note");
      }, 0);
      return () => clearTimeout(timeoutId);
    }
  }, [
    purchaseOrder,
    brand,
    receiveQty,
    debouncedQty,
    basketWidth,
    plantCode,
    note,
  ]);

  // --- Table & Pagination States ---
  const [tableData, setTableData] = useState<BasketData[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(96);
  const [selectedRows, setSelectedRows] = useState<BasketData[]>([]);
  // const [pageData, setPageData] = useState<BasketData[]>([]);
  // const [loadedPages, setLoadedPages] = useState<Set<number>>(new Set());

  function deleteRows(rows: BasketData[]) {
    if (rows.length === 0) return;

    const deleteKeys = new Set(rows.map((r) => r.basket_no));

    setTableData((prev) =>
      prev.filter((row) => !deleteKeys.has(row.basket_no))
    );
  }

  function fileDownload(rows: BasketData[]) {
    console.log("Selected rows:", rows);

    showModal({
      type: "success",
      title: "Download Excel file",
      content: `Excel file downloaded with ${rows.length} items successfully!`,
    });
  }

  function printRFIDTags(rows: BasketData[]) {
    console.log("Selected rows:", rows);

    showModal({
      type: "success",
      title: "Print RFID tags",
      content: `${rows.length} RFID tags printed successfully!`,
    });
  }

  const actionButtons: ActionButton<BasketData>[] = [
    {
      icon: <Printer />,
      tooltip: "Print RFID Tags",
      onClick: printRFIDTags,
      disabled: false,
    },
    {
      icon: <FileDown />,
      color: "#00a944",
      tooltip: "Download Excel",
      onClick: fileDownload,
    },
  ];

  const paginatedData = tableData.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // --- Pagination Configuration ---

  // const handlePageChange = async (page: number) => {
  //   setCurrentPage(page);

  //   if (loadedPages.has(page)) {
  //     // Already fetched → just slice
  //     setPageData(
  //       tableData.slice((page - 1) * itemsPerPage, page * itemsPerPage)
  //     );
  //     return;
  //   }

  //   Fetch new page
  //   const response = await fetchBaskets({ page, size: itemsPerPage });

  //   setFullData((prev) => {
  //     const merged = [...prev, ...response.items];

  //     // Deduplicate by key
  //     return Array.from(
  //       new Map(merged.map((item) => [item.basket_no, item])).values()
  //     );
  //   });

  //   setLoadedPages((prev) => new Set(prev).add(page));
  //   setPageData(response.items);
  // };

  const paginationConfig: PaginationConfig = {
    currentPage: currentPage,
    itemsPerPage: itemsPerPage,
    totalItems: tableData.length,
    onPageChange: (page: number) => {
      setCurrentPage(page);
      // handlePageChange(page)
    },
    onItemsPerPageChange: (perPage: number) => {
      setItemsPerPage(perPage);
      setCurrentPage(1);
    },
    itemsPerPageOptions: [50, 96, 200, 500, 1000],
  };

  useEffect(() => {
    setTimeout(() => {
      setCurrentPage(1);
    }, 0);
  }, [tableData.length]);

  // --- Logic: Generate Rows ---

  function addNewData(reset: boolean = false) {
    const qty = parseInt(receiveQty);

    setTableData((prev) => {
      const baseData = reset ? [] : prev;

      const newRows: BasketData[] = Array.from({ length: qty }).map((_, i) => ({
        basket_no: `${plantCode}251226${String(
          baseData.length + i + 1
        ).padStart(8, "0")}`,
        brand: brand || "",
        capacity: capacity,
        length: basketWidth === "std" ? "682*415*105" : "Custom",
        received_date: receiveDate,
        purchase_order: purchaseOrder,
        create_group: new Date()
          .toISOString()
          .replace(/[-:T.Z]/g, "")
          .slice(0, 14),
      }));

      return [...baseData, ...newRows];
    });

    addToast("Basket added successfully", "success");
  }

  const handleAdd = () => {
    if (!purchaseOrder || !brand || !receiveQty) {
      addToast("Please fill in all required fields", "warning");
      return;
    }

    if (tableData.length > 0) {
      showModal({
        type: "confirm",
        title: "Delete Previous Basket?",
        content: "This action cannot be undone.",
        confirmText: "Delete",
        cancelText: "Keep",
        onCancel: () => addNewData(),
        onConfirm: () => addNewData(true),
      });
    } else {
      addNewData()
    }
  };

  const tableHeaders: TableHeader<BasketData>[] = [
    { title: "Basket No", isSortable: true, dataKey: "basket_no" },
    { title: "Brand", isSortable: true, dataKey: "brand" },
    { title: "Capacity", isSortable: true, dataKey: "capacity" },
    { title: "Length", isSortable: true, dataKey: "length" },
    { title: "Received Date", isSortable: true, dataKey: "received_date" },
    { title: "Purchase Order", isSortable: true, dataKey: "purchase_order" },
    { title: "Create Group", isSortable: true, dataKey: "create_group" },
  ];

  return (
    <Base
      currentApp={props.currentApp}
      navigateApp={props.navigateApp}
      navigatePage={props.navigatePage}
    >
      <div className="container mx-auto">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* 1. Purchase Order - Pulses until 10 chars are reached */}
            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                purchaseOrder.length < 10
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Input
                label="Purchase Order"
                required
                isFocus={focusField === "po"}
                value={purchaseOrder}
                onChange={(v: string) => setPurchaseOrder(v.slice(0, 10))}
                placeholder="10 characters required"
              />
            </div>

            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                purchaseOrder.length === 10 && !brand
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Dropdown
                label="Brand"
                required
                placeholder="Enter brand"
                isFocus={focusField === "brand"}
                isSearch={true}
                disabled={purchaseOrder.length < 10}
                value={brand}
                options={[
                  { label: "Nike", value: "nike" },
                  { label: "Adidas", value: "adidas" },
                ]}
                onChange={(v) => {
                  setBrand(v);
                  setFocusField("qty");
                }}
              />
            </div>

            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                brand && !receiveQty
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Input
                label="Receive Qty"
                required
                isFocus={focusField === "qty"}
                disabled={!brand}
                value={receiveQty}
                onChange={(v: string) => {
                  setReceiveQty(v);
                }}
                placeholder="e.g. 5"
              />
            </div>

            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                receiveQty && !basketWidth && debouncedQty
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Dropdown
                label="Basket width"
                required
                isFocus={focusField === "width"}
                isSearch={true}
                disabled={!receiveQty}
                value={basketWidth}
                options={[{ label: "Standard", value: "std" }]}
                onChange={(v) => {
                  setBasketWidth(v);
                  setFocusField("plant");
                }}
              />
            </div>

            <div className="p-1">
              <DatePicker
                label="Receive Date"
                required
                disabled={!basketWidth}
                type="day"
                value={receiveDate}
                onChange={(v: string) => setReceiveDate(v)}
              />
            </div>

            <div className="p-1">
              <Input
                label="Capacity"
                required
                disabled={!basketWidth}
                value={capacity}
                onChange={(v: string) => setCapacity(v)}
              />
            </div>

            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                basketWidth && !plantCode
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Dropdown
                label="Plant code"
                options={[
                  { label: "3001", value: "3001" },
                  { label: "3002", value: "3002" },
                ]}
                required
                isFocus={focusField === "plant"}
                isTyping={true}
                isSearch={true}
                disabled={!basketWidth}
                value={plantCode}
                onChange={(v: string) => {
                  setPlantCode(v);
                  setFocusField("note");
                }}
              />
            </div>

            <div
              className={`p-1 rounded-lg transition-all duration-500 ${
                plantCode && !note
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <Input
                label="Note"
                isFocus={focusField === "note"}
                disabled={!basketWidth}
                value={note}
                onChange={(v: string) => setNote(v)}
              />
            </div>
          </div>

          <div className="flex justify-center gap-4 mt-8">
            <div
              className={`rounded-lg transition-all duration-500 ${
                plantCode
                  ? "ring-2 ring-indigo-400 ring-offset-2 rounded-xl transition-all shadow-lg"
                  : "ring-0"
              }`}
            >
              <button
                onClick={handleAdd}
                className="flex items-center gap-2 px-10 py-3 bg-green-600 text-white rounded-lg font-bold shadow-lg hover:bg-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                disabled={!basketWidth || !receiveQty}
              >
                <PlusCircle size={20} />
                Add to Table
              </button>
            </div>

            <button
              onClick={() => deleteRows(selectedRows)}
              disabled={selectedRows.length <= 0}
              className="flex items-center gap-2 px-8 py-3 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
            >
              <Trash2 size={20} />
              Delete
            </button>
          </div>
        </div>

        <Table<BasketData>
          data={paginatedData}
          fullData={tableData}
          rowKey={"basket_no"}
          headers={tableHeaders}
          isCheckbox={true}
          isDivided={true}
          width="100%"
          maxHeight="45vh"
          onSelectionChange={(rows) => {
            setSelectedRows(rows);
          }}
          actionButtons={actionButtons}
          pagination={paginationConfig}
          informationElement={
            <div className="font-bold uppercase text-xs tracking-wider text-gray-500">
              Total items:{" "}
              <span className="text-indigo-600 ml-1">{tableData.length}</span>
            </div>
          }
        />
      </div>
    </Base>
  );
};

export default AddBasketPage;
