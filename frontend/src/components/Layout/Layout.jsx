import React, { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';


import CopilotWidget from '../CopilotWidget';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-neutral-50 relative">
      <Header toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex">
        <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen((open) => !open)} />
        <main className={`flex-1 p-6 transition-all duration-200 ${sidebarOpen ? 'ml-64' : 'ml-16'} min-h-[calc(100vh-61px)]`}>
          <div className="w-full">
            {children}
          </div>
        </main>
      </div>
      <CopilotWidget />
    </div>
  );
};

export default Layout;
