import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import {
  LayoutDashboard,
  FileText,
  Upload,
  BarChart3,
  Package,
  Shield,
  Mail,
  ChevronLeft,
  ChevronRight,
  Download
} from 'lucide-react';

const Sidebar = ({ isOpen, onToggle }) => {
  const { user } = useAuth();

  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard', description: 'Overview' },
    { path: '/rfps', icon: FileText, label: 'RFP List', description: 'All submissions' },
    { path: '/ingest', icon: Download, label: 'Ingest RFPs', description: 'Import & scrape' },
    { path: '/submit', icon: Upload, label: 'Submit RFP', description: 'New entry' },
    { path: '/emails', icon: Mail, label: 'Email Inbox', description: 'Discovered RFPs' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics', description: 'Insights' },
    { path: '/products', icon: Package, label: 'Products', description: 'Catalog' },
    { path: '/auditor', icon: Shield, label: 'Auditor', description: 'Compliance', adminOnly: true },
  ].filter(item => !item.adminOnly || user?.role === 'admin');

  return (
    <aside
      className={`fixed left-0 top-[61px] h-[calc(100vh-61px)] bg-olive-900 border-r border-olive-800 transition-all duration-200 ${isOpen ? 'w-64' : 'w-16'} z-40 flex flex-col shadow-xl`}
    >
      <button
        className="absolute -right-4 top-4 w-8 h-8 bg-olive-800 border border-olive-700 rounded-full flex items-center justify-center shadow-lg hover:bg-olive-700 transition text-olive-100"
        onClick={onToggle}
        aria-label={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        tabIndex={0}
      >
        {isOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
      </button>

      <nav className="p-3 space-y-1 mt-6">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center ${isOpen ? 'space-x-3 px-3 py-3' : 'justify-center py-3'} rounded-lg group transition-all duration-200 ${isActive
                ? 'bg-olive-800 text-white shadow-md border-l-4 border-olive-400'
                : 'text-olive-300 hover:bg-olive-800/50 hover:text-white'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <item.icon size={22} className={`transition-colors ${isActive ? 'text-olive-200' : 'text-olive-400 group-hover:text-olive-200'}`} />
                {isOpen && (
                  <div className="flex-1">
                    <div className="text-sm font-medium tracking-wide">{item.label}</div>
                    {/* Description hidden in dark compact mode to reduce clutter */}
                  </div>
                )}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className={`absolute bottom-0 left-0 right-0 p-4 border-t border-olive-800 bg-olive-900/50 ${isOpen ? '' : 'hidden'}`}>
        <div className="text-xs text-olive-400 space-y-2">
          <div className="font-semibold text-olive-300 uppercase tracking-wider text-[10px]">System Status</div>
          <div className="flex items-center justify-between p-2 bg-olive-950/50 rounded border border-olive-800">
            <span className="font-medium">Orchestrator</span>
            <div className="flex items-center space-x-1.5">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              <span className="text-green-400 font-medium">Online</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
