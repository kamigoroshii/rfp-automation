
import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileText,
  Upload,
  BarChart3,
  Package,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const Sidebar = ({ isOpen, onToggle }) => {
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard', description: 'Overview' },
    { path: '/rfps', icon: FileText, label: 'RFP List', description: 'All submissions' },
    { path: '/submit', icon: Upload, label: 'Submit RFP', description: 'New entry' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics', description: 'Insights' },
    { path: '/products', icon: Package, label: 'Products', description: 'Catalog' },
  ];

  return (
    <aside
      className={`fixed left-0 top-[61px] h-[calc(100vh-61px)] bg-olive-50 border-r border-olive-200 transition-all duration-200 ${isOpen ? 'w-64' : 'w-16'} z-40 flex flex-col`}
    >
      <button
        className="absolute -right-4 top-4 w-8 h-8 bg-olive-100 border border-olive-300 rounded-full flex items-center justify-center shadow-sm hover:bg-olive-200 transition"
        onClick={onToggle}
        aria-label={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        tabIndex={0}
      >
        {isOpen ? <ChevronLeft size={20} className="text-olive-700" /> : <ChevronRight size={20} className="text-olive-700" />}
      </button>
      <nav className="p-3 space-y-1 mt-8">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center ${isOpen ? 'space-x-3 px-3 py-2.5' : 'justify-center py-2'} rounded-md group transition-colors duration-100 ${
                isActive
                  ? 'bg-olive-100 text-olive-800 border-l-2 border-olive-500'
                  : 'text-olive-700 hover:bg-olive-200'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <item.icon size={22} className={isActive ? 'text-olive-700' : 'text-olive-500'} />
                {isOpen && (
                  <div className="flex-1">
                    <div className="text-sm font-semibold">{item.label}</div>
                    <div className="text-xs text-olive-500">{item.description}</div>
                  </div>
                )}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className={`absolute bottom-0 left-0 right-0 p-4 border-t border-olive-200 ${isOpen ? '' : 'hidden'}`}>
        <div className="text-xs text-olive-500 space-y-1">
          <div className="font-semibold text-olive-700">System Status</div>
          <div className="flex items-center justify-between">
            <span>Active</span>
            <div className="flex items-center space-x-1">
              <div className="w-1.5 h-1.5 bg-success rounded-full"></div>
              <span className="text-success">Online</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
