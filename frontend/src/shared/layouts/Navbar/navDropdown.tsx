import { ReactNode, useState } from "react";
// Suggestion: Install lucide-react for modern icons
import { ChevronDown } from "lucide-react"; 

export interface NavDropdownItem {
  label: string;
  navigate: string;
  icon?: ReactNode;
}

export interface NavDropdownGroup {
  label: string;
  icon?: ReactNode;
  items: NavDropdownItem[];
}

interface Props {
  group: NavDropdownGroup;
  onNavigate: (page: string) => void;
}

export const NavDropdown = ({ group, onNavigate }: Props) => {
  const [open, setOpen] = useState(false);

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      {/* Trigger Button */}
      <button
        type="button"
        className={`
          flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 cursor-pointer
          ${open ? "bg-blue-50 text-blue-700" : "bg-transparent text-gray-700 hover:bg-gray-100"}
        `}
      >
        <span className="opacity-70">{group.icon}</span>
        {group.label}
        <ChevronDown 
          className={`w-4 h-4 transition-transform duration-300 ${open ? "rotate-180" : ""}`} 
        />
      </button>

      {/* Dropdown Container with "The Bridge" */}
      <div 
        className={`
          absolute left-0 w-60 pt-2 z-50 transition-all duration-200 origin-top-left
          ${open ? "opacity-100 translate-y-0 scale-100" : "opacity-0 translate-y-2 scale-95 pointer-events-none"}
        `}
      >
        <div className="bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden ring-1 ring-blue-500">
          <ul className="p-1.5">
            {group.items.map((item) => (
              <li key={item.navigate}>
                <button
                  type="button"
                  onClick={() => {
                    onNavigate(item.navigate);
                    setOpen(false);
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2.5 text-sm text-gray-600 rounded-lg hover:bg-blue-50 hover:text-blue-700 transition-colors group cursor-pointer"
                >
                  {item.icon && (
                    <span className="text-gray-400 group-hover:text-blue-500 transition-colors">
                      {item.icon}
                    </span>
                  )}
                  <span className="font-medium">{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};