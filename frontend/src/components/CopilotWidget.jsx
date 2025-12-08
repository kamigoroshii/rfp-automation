import React, { useState } from 'react';
import { MessageSquare, X } from 'lucide-react';

const CopilotWidget = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {/* Iframe Modal */}
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <div
                        className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
                        onClick={() => setIsOpen(false)}
                    />

                    {/* Iframe Container */}
                    <div className="fixed inset-0 flex items-center justify-center z-50 p-4">
                        <div className="relative w-full max-w-2xl h-[600px] bg-white rounded-2xl shadow-2xl overflow-hidden">
                            {/* Close Button */}
                            <button
                                onClick={() => setIsOpen(false)}
                                className="absolute top-4 right-4 z-10 p-2 bg-white/90 hover:bg-white rounded-full shadow-lg transition-all"
                            >
                                <X size={20} className="text-gray-700" />
                            </button>

                            {/* Iframe */}
                            <iframe
                                src="/chat.html"
                                className="w-full h-full border-0"
                                title="RFP Copilot Chat"
                            />
                        </div>
                    </div>
                </>
            )}

            {/* Floating Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
                    w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300
                    ${isOpen
                        ? 'bg-white text-gray-600 hover:bg-gray-50 ring-2 ring-gray-100'
                        : 'bg-olive-600 text-white hover:bg-olive-700 hover:scale-110 ring-4 ring-olive-100'}
                `}
            >
                {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
            </button>
        </div>
    );
};

export default CopilotWidget;
