import React from 'react';
import { Menu, Bell, User } from 'lucide-react';

const Header = ({ toggleSidebar }) => {
  return (
    <header className="bg-white border-b border-neutral-200 sticky top-0 z-50 shadow-sm">
      <div className="flex items-center justify-between px-6 py-3.5">
        <div className="flex items-center space-x-3">
          <button
            onClick={toggleSidebar}
            className="p-2 rounded-md text-neutral-600 hover:bg-neutral-100"
            aria-label="Toggle Sidebar"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-md flex items-center justify-center">
              <span className="text-white font-bold text-sm">RF</span>
            </div>
            <div>
              <h1 className="text-base font-semibold text-neutral-900">RFP Automation</h1>
              <p className="text-xs text-neutral-500">Enterprise System</p>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button className="p-2 rounded-md text-neutral-600 hover:bg-neutral-100 relative">
            <Bell size={18} />
            <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-error rounded-full"></span>
          </button>
          <div className="h-6 w-px bg-neutral-200 mx-2"></div>
          <button className="flex items-center space-x-2 px-3 py-1.5 rounded-md hover:bg-neutral-100">
            <div className="w-7 h-7 bg-primary-100 rounded-full flex items-center justify-center">
              <User size={16} className="text-primary-700" />
            </div>
            <span className="text-sm font-medium text-neutral-700">Admin</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
