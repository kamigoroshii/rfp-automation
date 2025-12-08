import React, { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, TrendingUp, FileText } from 'lucide-react';

const AuditorDashboard = () => {
    const [auditStats, setAuditStats] = useState({
        total_audits: 0,
        approved: 0,
        flagged: 0,
        rejected: 0,
        avg_compliance_score: 0
    });

    const [recentAudits, setRecentAudits] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAuditData();
    }, []);

    const loadAuditData = async () => {
        try {
            // Mock data for now - will connect to real API later
            setAuditStats({
                total_audits: 45,
                approved: 32,
                flagged: 8,
                rejected: 5,
                avg_compliance_score: 0.87
            });

            setRecentAudits([
                {
                    rfp_id: 'RFP-2025-001',
                    title: 'Supply of 11kV XLPE Cables',
                    audit_timestamp: '2025-12-08T10:30:00Z',
                    overall_recommendation: 'APPROVE',
                    compliance_score: 0.94,
                    critical_issues_count: 0,
                    summary: 'RFP is compliant. Product matches are good. Pricing is competitive.'
                },
                {
                    rfp_id: 'RFP-2025-002',
                    title: 'HT Cable Supply for Industrial Plant',
                    audit_timestamp: '2025-12-08T09:15:00Z',
                    overall_recommendation: 'REVIEW',
                    compliance_score: 0.78,
                    critical_issues_count: 2,
                    summary: 'RFP has 2 compliance issues. Product matches need review. Pricing has issues.'
                },
                {
                    rfp_id: 'RFP-2025-003',
                    title: 'LT Power Cable for Commercial Building',
                    audit_timestamp: '2025-12-08T08:00:00Z',
                    overall_recommendation: 'APPROVE',
                    compliance_score: 0.91,
                    critical_issues_count: 0,
                    summary: 'RFP is compliant. Product matches are acceptable. Pricing is acceptable.'
                }
            ]);
        } catch (error) {
            console.error('Error loading audit data:', error);
        } finally {
            setLoading(false);
        }
    };

    const getRecommendationColor = (recommendation) => {
        switch (recommendation) {
            case 'APPROVE':
                return 'bg-green-100 text-green-800 border-green-200';
            case 'REVIEW':
                return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            case 'REJECT':
                return 'bg-red-100 text-red-800 border-red-200';
            default:
                return 'bg-gray-100 text-gray-800 border-gray-200';
        }
    };

    const getRecommendationIcon = (recommendation) => {
        switch (recommendation) {
            case 'APPROVE':
                return <CheckCircle className="text-green-600" size={20} />;
            case 'REVIEW':
                return <AlertTriangle className="text-yellow-600" size={20} />;
            case 'REJECT':
                return <XCircle className="text-red-600" size={20} />;
            default:
                return <FileText className="text-gray-600" size={20} />;
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div>
                <div className="flex items-center gap-3 mb-2">
                    <Shield className="text-primary" size={32} />
                    <h2 className="text-3xl font-bold text-text">Auditor Dashboard</h2>
                </div>
                <p className="text-text-light">Compliance validation and quality assurance</p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Total Audits</span>
                        <FileText className="text-blue-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-text">{auditStats.total_audits}</div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Approved</span>
                        <CheckCircle className="text-green-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-green-600">{auditStats.approved}</div>
                    <div className="text-xs text-text-light mt-1">
                        {((auditStats.approved / auditStats.total_audits) * 100).toFixed(0)}% approval rate
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Flagged</span>
                        <AlertTriangle className="text-yellow-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-yellow-600">{auditStats.flagged}</div>
                    <div className="text-xs text-text-light mt-1">Needs review</div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Rejected</span>
                        <XCircle className="text-red-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-red-600">{auditStats.rejected}</div>
                    <div className="text-xs text-text-light mt-1">Failed compliance</div>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Avg Compliance</span>
                        <TrendingUp className="text-primary" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-primary">
                        {(auditStats.avg_compliance_score * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-text-light mt-1">Overall score</div>
                </div>
            </div>

            {/* Recent Audits */}
            <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-text mb-4">Recent Audit Reports</h3>

                <div className="space-y-4">
                    {recentAudits.map((audit) => (
                        <div
                            key={audit.rfp_id}
                            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                        >
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h4 className="font-semibold text-text">{audit.title}</h4>
                                        <span className="text-sm text-text-light">{audit.rfp_id}</span>
                                    </div>
                                    <p className="text-sm text-text-light">{audit.summary}</p>
                                </div>

                                <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${getRecommendationColor(audit.overall_recommendation)}`}>
                                    {getRecommendationIcon(audit.overall_recommendation)}
                                    <span className="text-sm font-medium">{audit.overall_recommendation}</span>
                                </div>
                            </div>

                            <div className="flex items-center gap-6 text-sm">
                                <div className="flex items-center gap-2">
                                    <span className="text-text-light">Compliance Score:</span>
                                    <span className="font-semibold text-primary">
                                        {(audit.compliance_score * 100).toFixed(0)}%
                                    </span>
                                </div>

                                <div className="flex items-center gap-2">
                                    <span className="text-text-light">Critical Issues:</span>
                                    <span className={`font-semibold ${audit.critical_issues_count > 0 ? 'text-red-600' : 'text-green-600'}`}>
                                        {audit.critical_issues_count}
                                    </span>
                                </div>

                                <div className="flex items-center gap-2">
                                    <span className="text-text-light">Audited:</span>
                                    <span className="text-text">
                                        {new Date(audit.audit_timestamp).toLocaleString()}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Compliance Guidelines */}
            <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-text mb-4">Compliance Criteria</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border-l-4 border-green-500 pl-4">
                        <h4 className="font-semibold text-text mb-2">RFP Validation</h4>
                        <ul className="text-sm text-text-light space-y-1">
                            <li>✓ Complete title and scope</li>
                            <li>✓ Valid deadline (3-180 days)</li>
                            <li>✓ Required specifications present</li>
                            <li>✓ Testing requirements defined</li>
                        </ul>
                    </div>

                    <div className="border-l-4 border-blue-500 pl-4">
                        <h4 className="font-semibold text-text mb-2">Match Validation</h4>
                        <ul className="text-sm text-text-light space-y-1">
                            <li>✓ Match score ≥ 70%</li>
                            <li>✓ Specification alignment verified</li>
                            <li>✓ Multiple options available</li>
                            <li>✓ Product diversity checked</li>
                        </ul>
                    </div>

                    <div className="border-l-4 border-yellow-500 pl-4">
                        <h4 className="font-semibold text-text mb-2">Pricing Validation</h4>
                        <ul className="text-sm text-text-light space-y-1">
                            <li>✓ Positive unit prices</li>
                            <li>✓ Calculation accuracy</li>
                            <li>✓ Testing cost ≤ 15% of subtotal</li>
                            <li>✓ Delivery cost ≤ 10% of subtotal</li>
                        </ul>
                    </div>

                    <div className="border-l-4 border-purple-500 pl-4">
                        <h4 className="font-semibold text-text mb-2">Historical Comparison</h4>
                        <ul className="text-sm text-text-light space-y-1">
                            <li>✓ Price deviation ≤ 25%</li>
                            <li>✓ Anomaly detection active</li>
                            <li>✓ Competitive pricing verified</li>
                            <li>✓ Market trends considered</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AuditorDashboard;
