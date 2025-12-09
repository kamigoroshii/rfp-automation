import React from 'react';
import { Link } from 'react-router-dom';
import {
    ArrowRight,
    FileText,
    Cpu,
    CheckCircle,
    Zap,
    Shield,
    BarChart3,
    Users
} from 'lucide-react';
import heroBg from '../assets/hero-bg.png';

const LandingPage = () => {
    return (
        <div className="min-h-screen bg-neutral-50 font-sans text-neutral-900">
            {/* Navigation */}
            <nav className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
                <div className="w-full px-6">
                    <div className="flex justify-between items-center h-16">
                        {/* Logo - Left Corner */}
                        <div className="flex items-center gap-2">
                            <img src="/favicon.png" alt="RFP Automation Logo" className="w-8 h-8 object-contain" />
                            <div>
                                <h1 className="text-lg font-bold text-gray-900 tracking-tight">RFP Automation</h1>
                                <p className="text-[9px] text-olive-600 font-semibold tracking-wider uppercase">Enterprise Edition</p>
                            </div>
                        </div>

                        {/* Login Button - Right Corner */}
                        <Link
                            to="/login"
                            className="px-5 py-2 bg-olive-700 text-white font-semibold rounded-full transition-all shadow-md hover:shadow-lg hover:bg-olive-800 flex items-center gap-2"
                        >
                            Login <ArrowRight size={16} />
                        </Link>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative overflow-hidden min-h-screen flex items-center">
                <div className="absolute inset-0 z-0 pointer-events-none">
                    <img src={heroBg} alt="Hero Background" className="w-full h-full object-cover" />
                    <div className="absolute inset-0 bg-white/15"></div>
                </div>

                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center w-full py-20">


                    <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-clip-text text-transparent bg-gradient-to-r from-olive-900 via-olive-800 to-olive-900 pb-2">
                        Turn RFPs into <br />
                        <span className="text-olive-600">Winning Proposals</span>
                    </h1>

                    <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
                        Automate the entire RFP lifecycle with AI. From document parsing to compliance auditing, reduce your response time by 90% and increase win rates.
                    </p>

                    <div className="flex justify-center gap-4">
                        <Link
                            to="/login"
                            className="px-8 py-4 bg-olive-700 text-white rounded-full font-semibold text-lg hover:bg-olive-800 transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
                        >
                            Get Started Now
                        </Link>
                        <a
                            href="#how-it-works"
                            className="px-8 py-4 bg-white text-gray-700 border border-gray-200 rounded-full font-semibold text-lg hover:bg-gray-50 transition-all shadow-sm hover:shadow-md"
                        >
                            View Demo
                        </a>
                    </div>
                </div>
            </section>

            {/* Automation Flow / Features */}
            <section id="how-it-works" className="py-24 bg-olive-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl font-bold text-gray-900">Seamless Automation Workflow</h2>
                        <p className="text-gray-500 mt-2">How our AI engine processes your requests</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
                        {/* Connecting Line */}
                        <div className="hidden md:block absolute top-[28px] left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-olive-200 to-transparent z-0"></div>

                        <FlowStep
                            icon={FileText}
                            step="1"
                            title="Ingest & Parse"
                            desc="AI extracts scope, specs, and requirements from PDF or Web."
                        />
                        <FlowStep
                            icon={Cpu}
                            step="2"
                            title="Match Products"
                            desc="Smart inventory matching based on extracted specifications."
                        />
                        <FlowStep
                            icon={CheckCircle}
                            step="3"
                            title="Generate & Audit"
                            desc="Auto-generate proposals and run compliance audits."
                        />
                        <FlowStep
                            icon={Zap}
                            step="4"
                            title="Submit & Track"
                            desc="One-click submission and real-time analytics tracking."
                        />
                    </div>
                </div>
            </section>

            {/* Feature Highlights Grid */}
            <section className="py-24 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        <FeatureCard
                            icon={Shield}
                            title="Built-in Auditor"
                            desc="Automatic compliance checks ensure you never submit a non-compliant proposal."
                        />
                        <FeatureCard
                            icon={BarChart3}
                            title="Real-time Analytics"
                            desc="Track win rates, processing times, and revenue forecasts in one dashboard."
                        />
                        <FeatureCard
                            icon={Users}
                            title="Team Collaboration"
                            desc="Role-based access control for Admins and Team members."
                        />
                    </div>
                </div>
            </section>

            {/* Testimonials */}
            <section className="py-24 bg-gradient-to-b from-olive-50 to-white relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl font-bold text-center text-gray-900 mb-16">Trusted by Industry Leaders</h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <TestimonialCard
                            quote="This platform reduced our proposal generation time from days to minutes. The accuracy is unmatched."
                            author="Sarah Johnson"
                            role="Procurement Head, Metro Rail Corp"
                            avatar="https://ui-avatars.com/api/?name=Sarah+Johnson&background=0D8ABC&color=fff"
                        />
                        <TestimonialCard
                            quote="The auditor feature is a lifesaver. We caught crucial compliance issues before submission."
                            author="Michael Chen"
                            role="Director, Solar Energy Ltd"
                            avatar="https://ui-avatars.com/api/?name=Michael+Chen&background=10B981&color=fff"
                        />
                        <TestimonialCard
                            quote="Seamless inventory integration. It automatically picks the best products for every RFP."
                            author="Priya Patel"
                            role="Operations Lead, Smart Infra City"
                            avatar="https://ui-avatars.com/api/?name=Priya+Patel&background=F59E0B&color=fff"
                        />
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-olive-800 text-white py-12 border-t border-olive-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                        <div className="col-span-1 md:col-span-2">
                            <div className="flex items-center gap-3 mb-4">
                                <div className="w-8 h-8 bg-olive-700 rounded-md flex items-center justify-center">
                                    <span className="font-bold text-sm">RF</span>
                                </div>
                                <span className="text-xl font-bold">RFP Automation</span>
                            </div>
                            <p className="text-olive-200 text-sm max-w-sm">
                                Empowering businesses to win more deals with AI-driven proposal automation and intelligent insights.
                            </p>
                        </div>

                        <div>
                            <h4 className="font-semibold mb-4">Product</h4>
                            <ul className="space-y-2 text-sm text-olive-200">
                                <li><a href="#" className="hover:text-white transition">Features</a></li>
                                <li><a href="#" className="hover:text-white transition">Security</a></li>
                                <li><a href="#" className="hover:text-white transition">Enterprise</a></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-semibold mb-4">Company</h4>
                            <ul className="space-y-2 text-sm text-gray-400">
                                <li><a href="#" className="hover:text-white transition">About Us</a></li>
                                <li><a href="#" className="hover:text-white transition">Contact</a></li>
                                <li><a href="#" className="hover:text-white transition">Careers</a></li>
                            </ul>
                        </div>
                    </div>

                    <div className="pt-8 border-t border-olive-700 flex flex-col md:flex-row justify-between items-center gap-4">
                        <p className="text-sm text-olive-300">© 2025 RFP Automation Inc. All rights reserved.</p>
                        <div className="flex gap-6">
                            <a href="#" className="text-olive-300 hover:text-white transition">Privacy Policy</a>
                            <a href="#" className="text-olive-300 hover:text-white transition">Terms of Service</a>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

const FlowStep = ({ icon: Icon, step, title, desc }) => (
    <div className="relative z-10 flex flex-col items-center text-center group">
        <div className="w-14 h-14 bg-white border-2 border-olive-100 rounded-2xl flex items-center justify-center mb-4 shadow-sm group-hover:shadow-md group-hover:border-olive-500 transition-all duration-300">
            <Icon size={24} className="text-olive-600" />
        </div>
        <div className="bg-olive-50 text-olive-800 text-xs font-bold px-2 py-1 rounded-full mb-2">Step {step}</div>
        <h3 className="font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-sm text-gray-500 leading-relaxed px-4">{desc}</p>
    </div>
);

const FeatureCard = ({ icon: Icon, title, desc }) => (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all duration-300">
        <div className="w-12 h-12 bg-olive-50 rounded-xl flex items-center justify-center mb-4 text-olive-600">
            <Icon size={24} />
        </div>
        <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-gray-600 text-sm leading-relaxed">{desc}</p>
    </div>
);

const TestimonialCard = ({ quote, author, role, avatar }) => (
    <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 relative">
        {/* Quote Icon */}
        <div className="absolute top-6 right-6 text-olive-200">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor">
                <path d="M14.017 21L14.017 18C14.017 16.8954 14.9124 16 16.017 16H19.017C19.5693 16 20.017 15.5523 20.017 15V9C20.017 8.44772 19.5693 8 19.017 8H15.017C14.4647 8 14.017 8.44772 14.017 9V11C14.017 11.5523 13.5693 12 13.017 12H12.017V5H22.017V15C22.017 18.3137 19.3307 21 16.017 21H14.017ZM5.0166 21L5.0166 18C5.0166 16.8954 5.91203 16 7.0166 16H10.0166C10.5689 16 11.0166 15.5523 11.0166 15V9C11.0166 8.44772 10.5689 8 10.0166 8H6.0166C5.46432 8 5.0166 8.44772 5.0166 9V11C5.0166 11.5523 4.56889 12 4.0166 12H3.0166V5H13.0166V15C13.0166 18.3137 10.3303 21 7.0166 21H5.0166Z" />
            </svg>
        </div>

        <p className="text-gray-700 mb-6 relative z-10 font-medium italic">"{quote}"</p>

        <div className="flex items-center gap-4">
            <img src={avatar} alt={author} className="w-12 h-12 rounded-full border-2 border-white shadow-sm" />
            <div>
                <h4 className="font-bold text-gray-900 text-sm">{author}</h4>
                <p className="text-xs text-gray-500">{role}</p>
            </div>
        </div>
    </div>
);

export default LandingPage;
