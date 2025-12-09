
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Globe, Mail, Upload, FileText, Download, Sparkles } from 'lucide-react';

const MOCK_URL_DATA = {
    'https://tenders.gov.in/rfp/metro-rail-cabling': {
        title: 'Urgent: 33kV Low Loss Cabling for Metro Phase IV',
        deadline: '2025-12-25T17:00',
        scope: 'Requirement for 25km of 33kV XLPE Underground Cables. \nSpecifications:\n- Voltage: 33kV\n- Conductor: Copper\n- Core: 3-Core\n- Armour: Steel Wire\n- Sheath: FRLS PVC',
        testing_requirements: 'Type Test, Routine Test, IEC 60502'
    },
    'https://solar-energy.corp/bids/50mw-module-supply': {
        title: 'Supply of 540Wp Mono-PERC Modules',
        deadline: '2026-01-15T12:00',
        scope: 'Procurement of 10,000 units of Mono PERC Solar Modules for 50MW Solar Park.\nRequired Specs:\n- Power Output: >540Wp\n- Efficiency: >21%\n- Technology: Mono PERC Half-Cut\n- Warranty: 25 Years Linear Performance',
        testing_requirements: 'EL Test, Flash Test, IEC 61215'
    },
    'https://smart-infra.city/tenders/smart-street-lights': {
        title: 'Smart LED Street Lighting Implementation',
        deadline: '2025-12-30T10:00',
        scope: 'Supply and installation of 500 Smart LED Street Lights with LoraWAN control.\nSpecs:\n- Wattage: 120W\n- Lumens: >14000lm\n- IP Rating: IP66\n- Control: LoraWAN NEMA Controller',
        testing_requirements: 'LM-79, LM-80, IP Test'
    }
};

const IngestRFPs = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('web');
    const [url, setUrl] = useState('');
    const [isScraping, setIsScraping] = useState(false);

    const handleScrape = async () => {
        if (!url) {
            toast.error('Please enter a URL');
            return;
        }

        setIsScraping(true);
        // Simulate extraction delay
        await new Promise(resolve => setTimeout(resolve, 1500));

        const data = MOCK_URL_DATA[url];

        setIsScraping(false);

        if (data) {
            toast.success('RFP Scraped Successfully!');
            // Navigate to SubmitRFP with pre-filled state
            navigate('/submit', {
                state: {
                    prefill: {
                        source: url,
                        ...data
                    }
                }
            });
        } else {
            // Fallback for unknown URL
            toast.success('RFP Scraped Successfully (Generic)!');
            navigate('/submit', {
                state: {
                    prefill: {
                        source: url,
                        title: 'Discovered RFP from URL',
                        scope: 'Content scraped from ' + url
                    }
                }
            });
        }
    };

    return (
        <div className="w-full space-y-6">
            <div>
                <h2 className="text-3xl font-bold text-gray-800">RFP Ingestion & Processing</h2>
                <p className="text-gray-500 mt-1">Import RFPs from web scraping, emails, or demo data</p>
            </div>

            {/* Tabs */}
            <div className="flex gap-8 border-b border-gray-200">
                <button
                    onClick={() => setActiveTab('web')}
                    className={`pb-3 px-1 font-medium transition-colors ${activeTab === 'web'
                        ? 'text-olive-700 border-b-2 border-olive-700'
                        : 'text-gray-500 hover:text-gray-700'}`}
                >
                    <div className="flex items-center gap-2">
                        <Globe size={18} />
                        Web Scraping
                    </div>
                </button>
                <button
                    onClick={() => setActiveTab('email')}
                    className={`pb-3 px-1 font-medium transition-colors ${activeTab === 'email'
                        ? 'text-olive-700 border-b-2 border-olive-700'
                        : 'text-gray-500 hover:text-gray-700'}`}
                >
                    <div className="flex items-center gap-2">
                        <Mail size={18} />
                        Email Import
                    </div>
                </button>
                <button
                    onClick={() => setActiveTab('demo')}
                    className={`pb-3 px-1 font-medium transition-colors ${activeTab === 'demo'
                        ? 'text-olive-700 border-b-2 border-olive-700'
                        : 'text-gray-500 hover:text-gray-700'}`}
                >
                    <div className="flex items-center gap-2">
                        <Upload size={18} />
                        Demo Data
                    </div>
                </button>
            </div>

            {/* Web Scraping Content */}
            {activeTab === 'web' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 min-h-[400px]">
                    <h3 className="text-xl font-bold text-gray-800 mb-6">Scrape RFPs from Website</h3>

                    <div className="max-w-3xl space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Website URL
                            </label>
                            <input
                                type="url"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                                placeholder="https://example.com/tenders"
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-olive-500 focus:border-transparent text-gray-700"
                            />
                        </div>

                        <button
                            onClick={handleScrape}
                            disabled={isScraping}
                            className="w-full py-4 bg-olive-600 hover:bg-olive-700 text-white font-semibold rounded-lg shadow transition-colors flex items-center justify-center gap-2 text-lg"
                        >
                            {isScraping ? (
                                <>
                                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                                    Scraping...
                                </>
                            ) : (
                                <>
                                    <Globe size={24} />
                                    Scrape Website
                                </>
                            )}
                        </button>

                        {/* Demo Chips */}
                        <div className="pt-4 border-t border-gray-100">
                            <p className="text-sm text-gray-500 mb-3">Or try these demo sources:</p>
                            <div className="flex flex-wrap gap-2">
                                {Object.keys(MOCK_URL_DATA).map((mockUrl) => (
                                    <button
                                        key={mockUrl}
                                        onClick={() => setUrl(mockUrl)}
                                        className="px-3 py-1.5 bg-gray-50 hover:bg-olive-50 text-olive-700 text-sm border border-gray-200 hover:border-olive-200 rounded-full transition-colors truncate max-w-md"
                                        title={MOCK_URL_DATA[mockUrl].title}
                                    >
                                        {mockUrl}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Email Import Content */}
            {activeTab === 'email' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 min-h-[400px]">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-bold text-gray-800">Email Import - Pending RFPs</h3>
                        <button
                            onClick={() => navigate('/emails')}
                            className="px-4 py-2 bg-olive-700 text-white font-semibold rounded-lg hover:bg-olive-800 transition-colors flex items-center gap-2"
                        >
                            <Mail size={18} />
                            Email Inbox
                        </button>
                    </div>

                    <div className="space-y-4">
                        {/* Email RFP 1 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Mail size={16} className="text-olive-600" />
                                        <span className="font-semibold text-gray-900">Hospital LED Lighting Upgrade - RFP</span>
                                    </div>
                                    <p className="text-sm text-gray-600">From: procurement@cityhospital.org</p>
                                    <p className="text-xs text-gray-500">Received: Dec 8, 2025 at 2:30 PM</p>
                                </div>
                                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">New</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Attached: <strong>Hospital_LED_RFP_2025.pdf</strong> (2.4 MB)</span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">Subject: Request for Proposal - LED Lighting System for 500-bed facility</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'procurement@cityhospital.org',
                                            title: 'Hospital LED Lighting Upgrade',
                                            deadline: '2025-12-28T17:00',
                                            scope: 'Supply and installation of energy-efficient LED lighting for entire 500-bed hospital facility',
                                            testing_requirements: 'Medical-grade certification, CRI >95, Emergency backup testing'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-olive-600 text-white text-sm font-medium rounded-lg hover:bg-olive-700 transition-colors"
                            >
                                Process RFP
                            </button>
                        </div>

                        {/* Email RFP 2 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Mail size={16} className="text-olive-600" />
                                        <span className="font-semibold text-gray-900">Solar Farm Development - 100MW Project</span>
                                    </div>
                                    <p className="text-sm text-gray-600">From: tenders@renewableenergy.gov</p>
                                    <p className="text-xs text-gray-500">Received: Dec 7, 2025 at 10:15 AM</p>
                                </div>
                                <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">New</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Attached: <strong>Solar_Farm_RFP_100MW.pdf</strong> (5.1 MB)</span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">Subject: RFP for 100MW Solar Farm - Module Supply & Installation</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'tenders@renewableenergy.gov',
                                            title: 'Solar Farm Development - 100MW',
                                            deadline: '2026-01-20T12:00',
                                            scope: '100MW solar farm requiring bifacial modules, inverters, and mounting structures',
                                            testing_requirements: 'IEC 61215, IEC 61730, Flash test, EL test'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-olive-600 text-white text-sm font-medium rounded-lg hover:bg-olive-700 transition-colors"
                            >
                                Process RFP
                            </button>
                        </div>

                        {/* Email RFP 3 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Mail size={16} className="text-olive-600" />
                                        <span className="font-semibold text-gray-900">Airport Terminal Lighting Modernization</span>
                                    </div>
                                    <p className="text-sm text-gray-600">From: procurement@internationalairport.com</p>
                                    <p className="text-xs text-gray-500">Received: Dec 6, 2025 at 4:45 PM</p>
                                </div>
                                <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">Reviewed</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Attached: <strong>Airport_Lighting_RFP.pdf</strong> (3.8 MB)</span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">Subject: Terminal 3 LED Lighting Upgrade - Request for Proposal</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'procurement@internationalairport.com',
                                            title: 'Airport Terminal Lighting Modernization',
                                            deadline: '2025-12-30T16:00',
                                            scope: 'Complete LED lighting replacement for Terminal 3 including emergency systems',
                                            testing_requirements: 'Aviation-grade certification, Emergency lighting duration test, IP65 rating'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-olive-600 text-white text-sm font-medium rounded-lg hover:bg-olive-700 transition-colors"
                            >
                                Process RFP
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Demo Data Content */}
            {activeTab === 'demo' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 min-h-[400px]">
                    <h3 className="text-xl font-bold text-gray-800 mb-6">Demo RFP Data</h3>

                    <div className="space-y-4">
                        {/* Demo RFP 1 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Sparkles size={16} className="text-purple-600" />
                                        <span className="font-semibold text-gray-900">Smart City Street Lighting - Phase 2</span>
                                    </div>
                                    <p className="text-sm text-gray-600">Demo Source: Smart City Initiative</p>
                                </div>
                                <span className="px-3 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">Demo</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Document: <strong>SmartCity_Lighting_Demo.pdf</strong></span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">1000 smart LED streetlights with IoT controls and energy monitoring</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'Demo Data - Smart City',
                                            title: 'Smart City Street Lighting - Phase 2',
                                            deadline: '2026-01-10T15:00',
                                            scope: 'Supply and installation of 1000 smart LED streetlights with LoRaWAN/NB-IoT connectivity',
                                            testing_requirements: 'IP66 rating, LM-79, LM-80, Surge protection 10kV'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 transition-colors"
                            >
                                Load Demo RFP
                            </button>
                        </div>

                        {/* Demo RFP 2 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Sparkles size={16} className="text-purple-600" />
                                        <span className="font-semibold text-gray-900">Industrial Warehouse LED Retrofit</span>
                                    </div>
                                    <p className="text-sm text-gray-600">Demo Source: Manufacturing Sector</p>
                                </div>
                                <span className="px-3 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">Demo</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Document: <strong>Warehouse_LED_Demo.pdf</strong></span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">High-bay LED lighting for 50,000 sq ft warehouse facility</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'Demo Data - Industrial',
                                            title: 'Industrial Warehouse LED Retrofit',
                                            deadline: '2025-12-22T12:00',
                                            scope: '200W high-bay LED fixtures for 50,000 sq ft warehouse with motion sensors',
                                            testing_requirements: 'DLC Premium, LM-79, Photometric testing, Vibration test'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 transition-colors"
                            >
                                Load Demo RFP
                            </button>
                        </div>

                        {/* Demo RFP 3 */}
                        <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <Sparkles size={16} className="text-purple-600" />
                                        <span className="font-semibold text-gray-900">Rooftop Solar Installation - Commercial Building</span>
                                    </div>
                                    <p className="text-sm text-gray-600">Demo Source: Green Energy Program</p>
                                </div>
                                <span className="px-3 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">Demo</span>
                            </div>
                            <div className="mt-3 flex items-center gap-2 text-sm">
                                <FileText size={14} className="text-gray-500" />
                                <span className="text-gray-700">Document: <strong>Rooftop_Solar_Demo.pdf</strong></span>
                            </div>
                            <p className="text-sm text-gray-600 mt-2">250kW rooftop solar system with net metering</p>
                            <button
                                onClick={() => navigate('/submit', {
                                    state: {
                                        prefill: {
                                            source: 'Demo Data - Solar',
                                            title: 'Rooftop Solar Installation - Commercial Building',
                                            deadline: '2026-01-05T17:00',
                                            scope: '250kW rooftop solar system with 540Wp modules, string inverters, and monitoring',
                                            testing_requirements: 'IEC 61215, IEC 61730, Inverter efficiency test, Grid compliance'
                                        }
                                    }
                                })}
                                className="mt-3 px-4 py-2 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 transition-colors"
                            >
                                Load Demo RFP
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default IngestRFPs;
