import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, Minimize2, Upload, Paperclip } from 'lucide-react';

const CopilotWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        {
            id: 1,
            type: 'bot',
            text: 'Hello! I am your RFP Copilot. I can help you analyze documents, compare specs, or answer questions about ongoing tenders. Upload a PDF to get started!',
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [uploadedFile, setUploadedFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        // Add user message
        const userMsg = {
            id: Date.now(),
            role: 'user',
            type: 'user',
            text: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMsg]);
        setInputValue('');
        setIsTyping(true);

        try {
            // Prepare history for API
            const historyForApi = messages.map(m => ({
                role: m.type === 'user' ? 'user' : 'model',
                content: m.text
            }));

            // Add current message
            historyForApi.push({
                role: 'user',
                content: inputValue // Note: inputValue is empty here because setInputValue was called, use userMsg.text
            });
            // Fix: Use the variable directly
            historyForApi[historyForApi.length - 1].content = userMsg.text;

            // Call API
            const response = await fetch('/api/copilot/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    messages: historyForApi
                })
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API Error Details:', response.status, response.statusText);
                console.error('API Error Body:', errorText);
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();

            // Add bot response
            const botResponse = {
                id: Date.now() + 1,
                type: 'bot',
                text: data.response,
                timestamp: new Date(data.timestamp)
            };

            setMessages(prev => [...prev, botResponse]);

        } catch (error) {
            console.error('Error calling Copilot API:', error);
            // Add error message
            const errorMsg = {
                id: Date.now() + 1,
                type: 'bot',
                text: "Sorry, I'm having trouble connecting to the server. Please try again later.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsTyping(false);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Validate file type
        if (file.type !== 'application/pdf') {
            const errorMsg = {
                id: Date.now(),
                type: 'bot',
                text: 'Please upload a PDF file only.',
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMsg]);
            return;
        }

        setIsUploading(true);
        setUploadedFile(file);

        // Add upload notification
        const uploadMsg = {
            id: Date.now(),
            type: 'bot',
            text: `📄 Uploading "${file.name}"... Please wait while I analyze the document.`,
            timestamp: new Date()
        };
        setMessages(prev => [...prev, uploadMsg]);

        try {
            // Create form data
            const formData = new FormData();
            formData.append('file', file);
            formData.append('title', file.name.replace('.pdf', ''));
            formData.append('source', `Copilot Upload: ${file.name}`);
            formData.append('deadline', new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString()); // 30 days from now
            formData.append('scope', 'Document uploaded via Copilot for analysis');
            formData.append('testing_requirements', '');

            // Upload to backend
            const response = await fetch('/api/rfp/submit', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const data = await response.json();

            // Success message
            const successMsg = {
                id: Date.now() + 1,
                type: 'bot',
                text: `✅ Document "${file.name}" uploaded successfully! I can now answer questions about this document. What would you like to know?`,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, successMsg]);

        } catch (error) {
            console.error('Error uploading file:', error);
            const errorMsg = {
                id: Date.now() + 1,
                type: 'bot',
                text: `❌ Sorry, there was an error uploading the file. Please try again.`,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end pointer-events-none">
            {/* Chat Window */}
            <div
                className={`
                    mb-4 w-[380px] h-[550px] bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden flex flex-col transition-all duration-300 origin-bottom-right pointer-events-auto
                    ${isOpen ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-4 pointer-events-none hidden'}
                `}
            >
                {/* Header */}
                <div className="bg-gradient-to-r from-olive-600 to-olive-800 p-4 flex items-center justify-between text-white shadow-md">
                    <div className="flex items-center space-x-3">
                        <div className="bg-white/20 p-2 rounded-full backdrop-blur-sm">
                            <Bot size={20} className="text-white" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-sm">RFP Copilot</h3>
                            <div className="flex items-center space-x-1.5 opacity-80">
                                <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></span>
                                <span className="text-xs">Online</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center space-x-1">
                        <button
                            onClick={() => setIsOpen(false)}
                            className="p-1.5 hover:bg-white/10 rounded-lg transition-colors"
                        >
                            <Minimize2 size={18} />
                        </button>
                    </div>
                </div>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4 scroll-smooth">
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`
                                    max-w-[80%] p-3.5 rounded-2xl text-sm shadow-sm
                                    ${msg.type === 'user'
                                        ? 'bg-olive-600 text-white rounded-br-none'
                                        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'}
                                `}
                            >
                                <p className="leading-relaxed">{msg.text}</p>
                                <span className={`text-[10px] block mt-1 ${msg.type === 'user' ? 'text-olive-100/80' : 'text-gray-400'}`}>
                                    {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                        </div>
                    ))}

                    {isTyping && (
                        <div className="flex justify-start">
                            <div className="bg-white border boundary-gray-200 px-4 py-3 rounded-2xl rounded-bl-none shadow-sm flex items-center space-x-1">
                                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-white border-t border-gray-100">
                    {/* Upload Button */}
                    <div className="mb-3">
                        <input
                            type="file"
                            ref={fileInputRef}
                            onChange={handleFileUpload}
                            accept=".pdf"
                            className="hidden"
                        />
                        <button
                            type="button"
                            onClick={() => fileInputRef.current?.click()}
                            disabled={isUploading}
                            className={`
                                w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border-2 border-dashed transition-all
                                ${isUploading
                                    ? 'border-gray-300 bg-gray-50 cursor-not-allowed'
                                    : 'border-olive-300 bg-olive-50 hover:bg-olive-100 hover:border-olive-400 cursor-pointer'
                                }
                            `}
                        >
                            {isUploading ? (
                                <>
                                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-olive-600"></div>
                                    <span className="text-sm text-olive-700">Uploading...</span>
                                </>
                            ) : (
                                <>
                                    <Upload size={16} className="text-olive-600" />
                                    <span className="text-sm font-medium text-olive-700">
                                        {uploadedFile ? `📄 ${uploadedFile.name}` : 'Upload PDF Document'}
                                    </span>
                                </>
                            )}
                        </button>
                    </div>

                    {/* Message Input */}
                    <form onSubmit={handleSendMessage} className="relative flex items-center">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Ask about uploaded documents..."
                            className="w-full bg-gray-50 text-gray-800 text-sm rounded-xl py-3 pl-4 pr-12 focus:outline-none focus:ring-2 focus:ring-olive-500/20 border border-gray-200 transition-all placeholder:text-gray-400"
                        />
                        <button
                            type="submit"
                            disabled={!inputValue.trim()}
                            className={`
                                absolute right-2 p-1.5 rounded-lg transition-all duration-200
                                ${inputValue.trim()
                                    ? 'bg-olive-600 text-white shadow-sm hover:transform hover:scale-105 active:scale-95'
                                    : 'bg-gray-100 text-gray-300 cursor-not-allowed'}
                            `}
                        >
                            <Send size={16} />
                        </button>
                    </form>
                    <div className="text-center mt-2">
                        <span className="text-[10px] text-gray-400">AI can make mistakes. Verify important info.</span>
                    </div>
                </div>
            </div>

            {/* Floating Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`
                    w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 pointer-events-auto
                    ${isOpen
                        ? 'bg-white text-gray-600 rotate-90 hover:bg-gray-50 ring-2 ring-gray-100'
                        : 'bg-olive-600 text-white hover:bg-olive-700 hover:scale-110 ring-4 ring-olive-100'}
                `}
            >
                {isOpen ? <X size={24} /> : <MessageSquare size={24} />}
            </button>
        </div>
    );
};

export default CopilotWidget;
