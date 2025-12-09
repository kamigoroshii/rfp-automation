import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Menu, Bell, User, AlertTriangle, Check, LogOut, ChevronDown } from 'lucide-react';

const Header = ({ toggleSidebar }) => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [notifications, setNotifications] = useState([
    // ... same notifications ...
    {
      id: 1,
      title: "High Value Opportunity Detected",
      message: "Medical Supplies Supply Chain RFP estimated at $2.5M",
      time: "10 mins ago",
      read: false
    },
    {
      id: 2,
      title: "Strategic Bid Alert",
      message: "Smart City Grid Expansion Project detected (> $10M)",
      time: "1 hour ago",
      read: false
    },
    {
      id: 3,
      title: "Urgent: High Priority",
      message: "IT Infrastructure Upgrade exceeds $1M threshold ($1.8M)",
      time: "2 hours ago",
      read: false
    }
  ]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAsRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  };

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })));
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

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
            <div className="w-8 h-8 bg-gradient-to-br from-olive-600 to-olive-800 rounded-md flex items-center justify-center">
              <span className="text-white font-bold text-sm">RF</span>
            </div>
            <div>
              <h1 className="text-base font-semibold text-neutral-900">RFP Automation</h1>
              <p className="text-xs text-neutral-500">Enterprise System</p>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2 relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2 rounded-md text-neutral-600 hover:bg-neutral-100 relative"
          >
            <Bell size={18} />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full ring-1 ring-white"></span>
            )}
          </button>

          {/* Notifications Dropdown */}
          {showNotifications && (
            <div className="absolute top-12 right-12 w-80 bg-white border border-gray-200 rounded-lg shadow-xl z-50 animate-in fade-in slide-in-from-top-2">
              <div className="p-3 border-b border-gray-100 flex justify-between items-center bg-gray-50 rounded-t-lg">
                <h3 className="font-semibold text-sm text-gray-800">Notifications ({unreadCount})</h3>
                {unreadCount > 0 && (
                  <button onClick={markAllRead} className="text-xs text-olive-600 hover:text-olive-700 font-medium">
                    Mark all read
                  </button>
                )}
              </div>
              <div className="max-h-[300px] overflow-y-auto">
                {notifications.map(n => (
                  <div key={n.id} className={`p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors ${n.read ? 'opacity-60' : 'bg-olive-50/10'}`}>
                    <div className="flex gap-3">
                      <div className="mt-1 flex-shrink-0">
                        <div className="w-8 h-8 bg-warning/10 rounded-full flex items-center justify-center">
                          <AlertTriangle size={14} className="text-warning" />
                        </div>
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <p className={`text-sm ${n.read ? 'font-medium' : 'font-bold'} text-gray-800`}>{n.title}</p>
                          {!n.read && (
                            <button onClick={(e) => { e.stopPropagation(); markAsRead(n.id); }} className="text-gray-400 hover:text-gray-600">
                              <Check size={14} />
                            </button>
                          )}
                        </div>
                        <p className="text-xs text-gray-600 mt-0.5 leading-snug">{n.message}</p>
                        <p className="text-[10px] text-gray-400 mt-1.5">{n.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="p-2 text-center border-t border-gray-100">
                <button onClick={() => setShowNotifications(false)} className="text-xs text-gray-500 hover:text-gray-700">Close</button>
              </div>
            </div>
          )}

          <div className="h-6 w-px bg-neutral-200 mx-2"></div>

          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 px-3 py-1.5 rounded-md hover:bg-neutral-100 transition-colors"
            >
              <div className="w-7 h-7 bg-olive-100 rounded-full flex items-center justify-center">
                <User size={16} className="text-olive-700" />
              </div>
              <span className="text-sm font-medium text-neutral-700 capitalize">
                {user?.username || 'Guest'}
              </span>
              <ChevronDown size={14} className="text-neutral-400" />
            </button>

            {showUserMenu && (
              <div className="absolute top-12 right-0 w-48 bg-white border border-gray-200 rounded-lg shadow-xl z-50 animate-in fade-in slide-in-from-top-2">
                <div className="p-3 border-b border-gray-100">
                  <p className="text-sm font-bold text-gray-800 capitalize">{user?.username}</p>
                  <p className="text-xs text-gray-500 capitalize">Role: {user?.role}</p>
                </div>
                <div className="p-1">
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
                  >
                    <LogOut size={16} />
                    Sign Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
