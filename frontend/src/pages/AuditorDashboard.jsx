import React, { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, TrendingUp, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { auditorAPI } from '../services/api';
import { useNavigate } from 'react-router-dom';

const AuditorDashboard = () => {
    const navigate = useNavigate();
    const [auditStats, setAuditStats] = useState({
        total_audits: 0,
        approved: 0,
        flagged: 0,
        rejected: 0,
        failed: 0,
        avg_compliance_score: 0
    });

    const [allAudits, setAllAudits] = useState([]);
    const [filteredAudits, setFilteredAudits] = useState([]);
    const [selectedFilter, setSelectedFilter] = useState('all');
    const [expandedAudit, setExpandedAudit] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadAuditData();
    }, []);

    useEffect(() => {
        filterAudits();
    }, [selectedFilter, allAudits]);

    const loadAuditData = async () => {
        try {
            setLoading(true);

            // Get audit reports from API
            const response = await auditorAPI.getReports();
            const reports = response.data.reports || [];
            const stats = response.data.stats || {};

            // Transform reports to match UI format
            const transformedReports = reports.map(report => ({
                rfp_id: report.rfp_id,
                title: report.rfp_title || 'Untitled RFP',
                audit_timestamp: report.audit_timestamp,
                overall_recommendation: report.overall_recommendation,
                compliance_score: report.compliance_score || 0,
                critical_issues_count: report.critical_issues_count || 0,
                summary: report.summary || 'No summary available',
                issues: report.issues || [],
                improvements: report.improvements || [],
                validation_results: report.validation_results || {}
            }));

            // Use static data if no reports from API
            if (transformedReports.length === 0) {
                const staticAudits = [
                    // APPROVED RFPs (7)
                    {
                        rfp_id: 'RFP-2025-001',
                        title: 'Metro Rail LED Lighting System',
                        audit_timestamp: '2025-12-08T14:30:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.98,
                        critical_issues_count: 0,
                        summary: 'All compliance checks passed. Product matches meet specifications with competitive pricing.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-002',
                        title: 'Solar Panel Installation - City Hall',
                        audit_timestamp: '2025-12-08T13:15:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.96,
                        critical_issues_count: 0,
                        summary: 'Excellent product alignment and pricing within acceptable range.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-003',
                        title: 'Smart Street Lighting Infrastructure',
                        audit_timestamp: '2025-12-08T11:45:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.94,
                        critical_issues_count: 0,
                        summary: 'Strong match scores and compliant pricing structure.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-004',
                        title: 'Industrial Warehouse LED Retrofit',
                        audit_timestamp: '2025-12-08T10:20:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.97,
                        critical_issues_count: 0,
                        summary: 'All validation criteria met with high confidence scores.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-005',
                        title: 'Airport Terminal Lighting Upgrade',
                        audit_timestamp: '2025-12-07T16:30:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.95,
                        critical_issues_count: 0,
                        summary: 'Comprehensive product coverage with competitive total estimate.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-006',
                        title: 'University Campus Solar Project',
                        audit_timestamp: '2025-12-07T15:10:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.93,
                        critical_issues_count: 0,
                        summary: 'Well-matched products with appropriate testing requirements.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-007',
                        title: 'Commercial Building Energy Efficiency',
                        audit_timestamp: '2025-12-07T14:00:00',
                        overall_recommendation: 'APPROVE',
                        compliance_score: 0.92,
                        critical_issues_count: 0,
                        summary: 'Solid proposal with verified product specifications.',
                        issues: [],
                        improvements: [],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: true }
                    },

                    // FLAGGED RFPs (8)
                    {
                        rfp_id: 'RFP-2025-101',
                        title: 'Highway LED Streetlight Replacement',
                        audit_timestamp: '2025-12-08T12:00:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.78,
                        critical_issues_count: 2,
                        summary: 'Minor compliance concerns requiring review before approval.',
                        issues: [
                            'Match score of 72% is below optimal threshold of 80%',
                            'Testing cost is 16% of subtotal, slightly above 15% guideline',
                            'Only 2 product options available, recommend 3+ for diversity'
                        ],
                        improvements: [
                            'Consider adding alternative product matches to improve diversity',
                            'Review testing requirements to optimize costs',
                            'Verify product specifications alignment with RFP requirements'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: false, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-102',
                        title: 'Municipal Solar Farm Development',
                        audit_timestamp: '2025-12-08T11:30:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.81,
                        critical_issues_count: 1,
                        summary: 'Pricing deviation from historical data requires verification.',
                        issues: [
                            'Total estimate 28% higher than similar historical projects',
                            'Delivery costs at 11% of subtotal exceed 10% guideline'
                        ],
                        improvements: [
                            'Negotiate delivery costs with suppliers',
                            'Review pricing against market benchmarks',
                            'Consider alternative logistics options'
                        ],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-103',
                        title: 'School District LED Conversion',
                        audit_timestamp: '2025-12-08T10:45:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.76,
                        critical_issues_count: 2,
                        summary: 'Specification alignment needs verification.',
                        issues: [
                            'Some product specifications do not fully match RFP requirements',
                            'Missing certification documentation for 2 products',
                            'Deadline is only 5 days away, may need extension request'
                        ],
                        improvements: [
                            'Obtain missing certifications from suppliers',
                            'Request deadline extension if needed',
                            'Verify all product specs meet minimum requirements'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-104',
                        title: 'Parking Garage Lighting Modernization',
                        audit_timestamp: '2025-12-07T17:20:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.79,
                        critical_issues_count: 1,
                        summary: 'Product diversity and testing requirements need attention.',
                        issues: [
                            'Limited product variety - only single manufacturer represented',
                            'Testing requirements incomplete for environmental conditions'
                        ],
                        improvements: [
                            'Include products from multiple manufacturers',
                            'Add environmental testing specifications',
                            'Expand product options for better pricing competition'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-105',
                        title: 'Stadium Floodlight Installation',
                        audit_timestamp: '2025-12-07T16:00:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.74,
                        critical_issues_count: 3,
                        summary: 'Multiple minor issues requiring clarification.',
                        issues: [
                            'Match confidence score at 74% needs improvement',
                            'Pricing calculations show minor discrepancies',
                            'Some testing requirements not clearly defined'
                        ],
                        improvements: [
                            'Recalculate pricing with updated unit costs',
                            'Clarify testing requirements with client',
                            'Improve product match scores through better specification alignment'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: false, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-106',
                        title: 'Residential Complex Solar Panels',
                        audit_timestamp: '2025-12-07T14:30:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.80,
                        critical_issues_count: 1,
                        summary: 'Historical pricing comparison shows anomaly.',
                        issues: [
                            'Price per unit 22% lower than historical average - verify supplier quotes',
                            'Warranty terms differ from standard offerings'
                        ],
                        improvements: [
                            'Confirm pricing accuracy with suppliers',
                            'Verify warranty terms are acceptable',
                            'Document reasons for pricing variance'
                        ],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: true, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-107',
                        title: 'Bridge Underpass Lighting System',
                        audit_timestamp: '2025-12-07T13:15:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.77,
                        critical_issues_count: 2,
                        summary: 'Scope definition and product matching need refinement.',
                        issues: [
                            'RFP scope description lacks specific technical details',
                            'Product matches based on limited specification data',
                            'Testing requirements may not cover all environmental factors'
                        ],
                        improvements: [
                            'Request additional technical specifications from client',
                            'Expand testing requirements for outdoor conditions',
                            'Refine product selection with more detailed criteria'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-108',
                        title: 'Factory Production Line LED Upgrade',
                        audit_timestamp: '2025-12-07T12:00:00',
                        overall_recommendation: 'REVIEW',
                        compliance_score: 0.82,
                        critical_issues_count: 1,
                        summary: 'Minor pricing and delivery concerns.',
                        issues: [
                            'Delivery timeline tight for quantity required',
                            'Installation costs not fully detailed'
                        ],
                        improvements: [
                            'Confirm supplier can meet delivery schedule',
                            'Break down installation costs by phase',
                            'Consider phased delivery if needed'
                        ],
                        validation_results: { rfp_valid: true, match_valid: true, pricing_valid: false, historical_valid: true }
                    },

                    // REJECTED RFPs (7)
                    {
                        rfp_id: 'RFP-2025-201',
                        title: 'Tunnel Lighting Emergency System',
                        audit_timestamp: '2025-12-08T09:30:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.42,
                        critical_issues_count: 5,
                        summary: 'Critical compliance failures - cannot proceed without major revisions.',
                        issues: [
                            'Match score of 45% is critically low - products do not meet specifications',
                            'Pricing exceeds historical average by 67% - not competitive',
                            'Missing mandatory safety certifications for tunnel applications',
                            'Testing requirements incomplete for emergency lighting standards',
                            'Deadline has already passed'
                        ],
                        improvements: [
                            'Completely revise product selection to meet RFP specifications',
                            'Obtain all required safety certifications before resubmission',
                            'Renegotiate pricing to competitive levels',
                            'Request deadline extension and clarify requirements',
                            'Add comprehensive emergency lighting testing protocols'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-202',
                        title: 'Hospital Operating Room Lighting',
                        audit_timestamp: '2025-12-08T08:15:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.38,
                        critical_issues_count: 6,
                        summary: 'Severe compliance violations in medical-grade requirements.',
                        issues: [
                            'Products lack required medical-grade certifications',
                            'Color rendering index (CRI) below medical standards (85 vs required 95+)',
                            'No emergency backup system specified',
                            'Pricing structure missing critical components',
                            'Testing requirements do not include medical compliance standards'
                        ],
                        improvements: [
                            'Source medical-grade certified products only',
                            'Ensure all products meet CRI 95+ requirement',
                            'Include emergency backup lighting system',
                            'Add comprehensive medical facility testing protocols',
                            'Complete pricing with all required components'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-203',
                        title: 'Offshore Platform Solar Installation',
                        audit_timestamp: '2025-12-07T18:45:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.51,
                        critical_issues_count: 4,
                        summary: 'Marine environment requirements not met.',
                        issues: [
                            'Products not rated for marine/saltwater environments',
                            'Missing corrosion resistance certifications',
                            'Installation methodology inadequate for offshore conditions',
                            'No contingency planning for weather delays'
                        ],
                        improvements: [
                            'Select marine-grade equipment with proper certifications',
                            'Include corrosion-resistant mounting systems',
                            'Develop offshore installation safety protocols',
                            'Add weather contingency timeline and costs'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: true, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-204',
                        title: 'Data Center Emergency Lighting',
                        audit_timestamp: '2025-12-07T17:30:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.47,
                        critical_issues_count: 5,
                        summary: 'Critical infrastructure requirements not satisfied.',
                        issues: [
                            'No redundancy systems specified for critical infrastructure',
                            'Battery backup duration insufficient (30min vs required 4hrs)',
                            'Products lack required uptime certifications',
                            'Missing integration with existing building management system',
                            'Maintenance plan inadequate for 24/7 operations'
                        ],
                        improvements: [
                            'Design fully redundant lighting system',
                            'Specify products with 4+ hour battery backup',
                            'Include BMS integration specifications',
                            'Develop comprehensive 24/7 maintenance plan',
                            'Obtain required uptime and reliability certifications'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: true, historical_valid: true }
                    },
                    {
                        rfp_id: 'RFP-2025-205',
                        title: 'Hazardous Area Industrial Lighting',
                        audit_timestamp: '2025-12-07T16:15:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.44,
                        critical_issues_count: 6,
                        summary: 'Explosion-proof requirements not met - safety critical.',
                        issues: [
                            'Products not explosion-proof rated for hazardous locations',
                            'Missing ATEX/IECEx certifications',
                            'Incorrect zone classification for products selected',
                            'No gas group compatibility verification',
                            'Installation procedures not compliant with safety standards'
                        ],
                        improvements: [
                            'Select only explosion-proof certified products',
                            'Obtain all required ATEX/IECEx certifications',
                            'Verify correct zone classification for each area',
                            'Document gas group compatibility',
                            'Develop safety-compliant installation procedures'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: true, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-206',
                        title: 'Military Base Perimeter Lighting',
                        audit_timestamp: '2025-12-07T15:00:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.39,
                        critical_issues_count: 7,
                        summary: 'Security and military specifications not addressed.',
                        issues: [
                            'Products do not meet military specifications (MIL-STD)',
                            'No security clearance documentation provided',
                            'Missing tamper-proof and ballistic-resistant features',
                            'Cybersecurity requirements for smart controls not addressed',
                            'No compliance with defense procurement regulations',
                            'Supplier not on approved vendor list'
                        ],
                        improvements: [
                            'Source MIL-STD certified products only',
                            'Obtain required security clearances',
                            'Include tamper-proof and ballistic-resistant options',
                            'Address cybersecurity requirements for all electronic components',
                            'Ensure supplier is on approved defense contractor list',
                            'Complete all defense procurement compliance documentation'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-207',
                        title: 'Clean Room Pharmaceutical Lighting',
                        audit_timestamp: '2025-12-07T14:15:00',
                        overall_recommendation: 'REJECT',
                        compliance_score: 0.49,
                        critical_issues_count: 5,
                        summary: 'Pharmaceutical clean room standards not met.',
                        issues: [
                            'Products not rated for ISO Class 5 clean room environments',
                            'Missing FDA compliance documentation',
                            'Fixtures not designed for easy cleaning/sterilization',
                            'No particle emission testing data provided',
                            'Lighting levels do not meet pharmaceutical inspection standards'
                        ],
                        improvements: [
                            'Select clean room certified lighting fixtures',
                            'Obtain FDA compliance certifications',
                            'Specify smooth, sealed fixtures for easy sterilization',
                            'Provide particle emission test results',
                            'Adjust lighting levels to meet pharmaceutical standards (1000+ lux)'
                        ],
                        validation_results: { rfp_valid: true, match_valid: false, pricing_valid: true, historical_valid: false }
                    },

                    // FAILED RFPs (8)
                    {
                        rfp_id: 'RFP-2025-301',
                        title: 'Incomplete RFP Submission - No Title',
                        audit_timestamp: '2025-12-08T07:00:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.15,
                        critical_issues_count: 8,
                        summary: 'Processing failed due to incomplete RFP data.',
                        issues: [
                            'RFP title missing or empty',
                            'Scope description not provided',
                            'No deadline specified',
                            'Testing requirements field empty',
                            'Unable to extract specifications from document'
                        ],
                        improvements: [
                            'Provide complete RFP title',
                            'Include detailed scope description',
                            'Specify clear deadline date',
                            'Define testing requirements',
                            'Ensure document is properly formatted and readable'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-302',
                        title: 'Corrupted PDF Upload',
                        audit_timestamp: '2025-12-08T06:30:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.08,
                        critical_issues_count: 9,
                        summary: 'Document parsing failed - file may be corrupted.',
                        issues: [
                            'PDF file could not be parsed',
                            'Document appears corrupted or password-protected',
                            'No text content extracted',
                            'Unable to process specifications'
                        ],
                        improvements: [
                            'Re-upload document in valid PDF format',
                            'Ensure PDF is not password-protected',
                            'Verify file is not corrupted',
                            'Consider using OCR if document is scanned'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-303',
                        title: 'Invalid Deadline Format',
                        audit_timestamp: '2025-12-07T19:15:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.22,
                        critical_issues_count: 6,
                        summary: 'Date parsing error - invalid deadline format.',
                        issues: [
                            'Deadline date format not recognized',
                            'Date appears to be in the past',
                            'Unable to calculate timeline for processing'
                        ],
                        improvements: [
                            'Use standard date format (YYYY-MM-DD)',
                            'Ensure deadline is in the future',
                            'Verify date is within acceptable range (3-180 days)'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-304',
                        title: 'Database Connection Error',
                        audit_timestamp: '2025-12-07T18:00:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.00,
                        critical_issues_count: 10,
                        summary: 'System error during processing - retry recommended.',
                        issues: [
                            'Database connection timeout',
                            'Unable to retrieve product catalog',
                            'Processing interrupted',
                            'System error - not RFP-related'
                        ],
                        improvements: [
                            'Retry submission',
                            'Contact system administrator if error persists',
                            'Check system status before resubmitting'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-305',
                        title: 'Missing Required Fields',
                        audit_timestamp: '2025-12-07T17:45:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.18,
                        critical_issues_count: 7,
                        summary: 'Multiple required fields missing from submission.',
                        issues: [
                            'Source field not specified',
                            'Scope description too brief (less than 10 words)',
                            'No specifications provided',
                            'Testing requirements missing'
                        ],
                        improvements: [
                            'Complete all required fields',
                            'Provide detailed scope (minimum 50 words)',
                            'Include technical specifications',
                            'Define testing requirements clearly'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-306',
                        title: 'Specification Extraction Failed',
                        audit_timestamp: '2025-12-07T16:45:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.25,
                        critical_issues_count: 5,
                        summary: 'AI unable to extract specifications from document.',
                        issues: [
                            'Document format not suitable for specification extraction',
                            'No structured technical data found',
                            'Unable to identify product requirements',
                            'Text too ambiguous for AI processing'
                        ],
                        improvements: [
                            'Provide specifications in structured format (tables, bullet points)',
                            'Use clear technical terminology',
                            'Include specific product requirements',
                            'Consider using RFP template for better results'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-307',
                        title: 'Duplicate RFP Submission',
                        audit_timestamp: '2025-12-07T15:30:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.30,
                        critical_issues_count: 4,
                        summary: 'Duplicate of existing RFP detected.',
                        issues: [
                            'RFP appears to be duplicate of RFP-2025-045',
                            'Same title and specifications as existing submission',
                            'Processing halted to prevent duplicate work'
                        ],
                        improvements: [
                            'Check existing RFPs before submitting',
                            'If resubmission is needed, update existing RFP instead',
                            'Contact administrator to remove duplicate'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    },
                    {
                        rfp_id: 'RFP-2025-308',
                        title: 'API Timeout During Processing',
                        audit_timestamp: '2025-12-07T14:45:00',
                        overall_recommendation: 'FAILED',
                        compliance_score: 0.12,
                        critical_issues_count: 8,
                        summary: 'Processing timeout - document too large or complex.',
                        issues: [
                            'Processing exceeded maximum time limit',
                            'Document may be too large (>50 pages)',
                            'Too many specifications to process in single request',
                            'System timeout error'
                        ],
                        improvements: [
                            'Split large RFPs into smaller sections',
                            'Reduce document size if possible',
                            'Simplify specification format',
                            'Retry submission during off-peak hours'
                        ],
                        validation_results: { rfp_valid: false, match_valid: false, pricing_valid: false, historical_valid: false }
                    }
                ];

                setAllAudits(staticAudits);
                setAuditStats({
                    total_audits: staticAudits.length,
                    approved: 7,
                    flagged: 8,
                    rejected: 7,
                    failed: 8,
                    avg_compliance_score: 0.72
                });
            } else {
                setAllAudits(transformedReports);

                // Calculate stats
                const approved = transformedReports.filter(r => r.overall_recommendation === 'APPROVE').length;
                const flagged = transformedReports.filter(r => r.overall_recommendation === 'REVIEW').length;
                const rejected = transformedReports.filter(r => r.overall_recommendation === 'REJECT').length;
                const failed = transformedReports.filter(r => r.overall_recommendation === 'FAILED').length;

                setAuditStats({
                    total_audits: transformedReports.length,
                    approved,
                    flagged,
                    rejected,
                    failed,
                    avg_compliance_score: stats.avg_compliance_score ||
                        (transformedReports.reduce((sum, r) => sum + r.compliance_score, 0) / transformedReports.length)
                });
            }

        } catch (error) {
            console.error('Error loading audit data:', error);
            // Fallback to empty state on error
            setAllAudits([]);
            setAuditStats({
                total_audits: 0,
                approved: 0,
                flagged: 0,
                rejected: 0,
                failed: 0,
                avg_compliance_score: 0
            });
        } finally {
            setLoading(false);
        }
    };

    const filterAudits = () => {
        if (selectedFilter === 'all') {
            setFilteredAudits(allAudits);
        } else {
            const statusMap = {
                'approved': 'APPROVE',
                'flagged': 'REVIEW',
                'rejected': 'REJECT',
                'failed': 'FAILED'
            };
            setFilteredAudits(allAudits.filter(audit =>
                audit.overall_recommendation === statusMap[selectedFilter]
            ));
        }
    };

    const handleStatusCardClick = (status) => {
        setSelectedFilter(status);
        setExpandedAudit(null);
    };

    const toggleAuditExpansion = (rfpId) => {
        setExpandedAudit(expandedAudit === rfpId ? null : rfpId);
    };

    const getRecommendationColor = (recommendation) => {
        switch (recommendation) {
            case 'APPROVE':
                return 'bg-green-100 text-green-800 border-green-200';
            case 'REVIEW':
                return 'bg-yellow-100 text-yellow-800 border-yellow-200';
            case 'REJECT':
                return 'bg-red-100 text-red-800 border-red-200';
            case 'FAILED':
                return 'bg-gray-100 text-gray-800 border-gray-200';
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
            case 'FAILED':
                return <XCircle className="text-gray-600" size={20} />;
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

            {/* Stats Cards - Now Clickable */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
                <button
                    onClick={() => handleStatusCardClick('all')}
                    className={`bg-white rounded-lg shadow-md p-6 text-left transition-all hover:shadow-lg ${selectedFilter === 'all' ? 'ring-2 ring-blue-500' : ''
                        }`}
                >
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Total Audits</span>
                        <FileText className="text-blue-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-text">{auditStats.total_audits}</div>
                    <div className="text-xs text-blue-600 mt-1">View All</div>
                </button>

                <button
                    onClick={() => handleStatusCardClick('approved')}
                    className={`bg-white rounded-lg shadow-md p-6 text-left transition-all hover:shadow-lg ${selectedFilter === 'approved' ? 'ring-2 ring-green-500' : ''
                        }`}
                >
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Approved</span>
                        <CheckCircle className="text-green-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-green-600">{auditStats.approved}</div>
                    <div className="text-xs text-text-light mt-1">
                        {auditStats.total_audits > 0 ? ((auditStats.approved / auditStats.total_audits) * 100).toFixed(0) : 0}% approval rate
                    </div>
                </button>

                <button
                    onClick={() => handleStatusCardClick('flagged')}
                    className={`bg-white rounded-lg shadow-md p-6 text-left transition-all hover:shadow-lg ${selectedFilter === 'flagged' ? 'ring-2 ring-yellow-500' : ''
                        }`}
                >
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Flagged</span>
                        <AlertTriangle className="text-yellow-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-yellow-600">{auditStats.flagged}</div>
                    <div className="text-xs text-text-light mt-1">Needs review</div>
                </button>

                <button
                    onClick={() => handleStatusCardClick('rejected')}
                    className={`bg-white rounded-lg shadow-md p-6 text-left transition-all hover:shadow-lg ${selectedFilter === 'rejected' ? 'ring-2 ring-red-500' : ''
                        }`}
                >
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Rejected</span>
                        <XCircle className="text-red-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-red-600">{auditStats.rejected}</div>
                    <div className="text-xs text-text-light mt-1">Failed compliance</div>
                </button>

                <button
                    onClick={() => handleStatusCardClick('failed')}
                    className={`bg-white rounded-lg shadow-md p-6 text-left transition-all hover:shadow-lg ${selectedFilter === 'failed' ? 'ring-2 ring-gray-500' : ''
                        }`}
                >
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-text-light text-sm">Failed</span>
                        <XCircle className="text-gray-500" size={20} />
                    </div>
                    <div className="text-3xl font-bold text-gray-600">{auditStats.failed}</div>
                    <div className="text-xs text-text-light mt-1">Processing errors</div>
                </button>

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

            {/* Filter Indicator */}
            {selectedFilter !== 'all' && (
                <div className="flex items-center gap-2 bg-blue-50 border border-blue-200 rounded-lg px-4 py-2">
                    <span className="text-sm text-blue-800">
                        Showing: <strong className="capitalize">{selectedFilter}</strong> RFPs ({filteredAudits.length})
                    </span>
                    <button
                        onClick={() => handleStatusCardClick('all')}
                        className="ml-auto text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                        Clear Filter
                    </button>
                </div>
            )}

            {/* Audit Reports List */}
            <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-text mb-4">
                    {selectedFilter === 'all' ? 'All Audit Reports' : `${selectedFilter.charAt(0).toUpperCase() + selectedFilter.slice(1)} RFPs`}
                </h3>

                <div className="space-y-4">
                    {filteredAudits.length === 0 ? (
                        <div className="text-center py-12 text-text-light">
                            <FileText className="mx-auto mb-4 text-gray-300" size={48} />
                            <p>No {selectedFilter !== 'all' ? selectedFilter : ''} audit reports found.</p>
                        </div>
                    ) : (
                        filteredAudits.map((audit) => (
                            <div
                                key={audit.rfp_id}
                                className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
                            >
                                {/* Main Audit Card */}
                                <div className="p-4">
                                    <div className="flex items-start justify-between mb-3">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3 mb-2">
                                                <h4
                                                    className="font-semibold text-text hover:text-primary cursor-pointer"
                                                    onClick={() => navigate(`/rfp/${audit.rfp_id}`)}
                                                >
                                                    {audit.title}
                                                </h4>
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

                                        {/* Expand/Collapse Button for non-approved RFPs */}
                                        {audit.overall_recommendation !== 'APPROVE' && (
                                            <button
                                                onClick={() => toggleAuditExpansion(audit.rfp_id)}
                                                className="ml-auto flex items-center gap-1 text-primary hover:text-primary-dark font-medium"
                                            >
                                                {expandedAudit === audit.rfp_id ? (
                                                    <>
                                                        <span>Hide Details</span>
                                                        <ChevronUp size={16} />
                                                    </>
                                                ) : (
                                                    <>
                                                        <span>View Details</span>
                                                        <ChevronDown size={16} />
                                                    </>
                                                )}
                                            </button>
                                        )}
                                    </div>
                                </div>

                                {/* Expanded Details Section */}
                                {expandedAudit === audit.rfp_id && audit.overall_recommendation !== 'APPROVE' && (
                                    <div className="border-t border-gray-200 bg-gray-50 p-6">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                            {/* Issues Section */}
                                            <div>
                                                <h5 className="font-semibold text-text mb-3 flex items-center gap-2">
                                                    <AlertTriangle className="text-red-500" size={18} />
                                                    Issues & Reasons
                                                </h5>
                                                {audit.issues && audit.issues.length > 0 ? (
                                                    <ul className="space-y-2">
                                                        {audit.issues.map((issue, idx) => (
                                                            <li key={idx} className="flex items-start gap-2 text-sm">
                                                                <span className="text-red-500 mt-0.5">•</span>
                                                                <span className="text-text-light">{issue}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                ) : (
                                                    <p className="text-sm text-text-light italic">No specific issues documented.</p>
                                                )}
                                            </div>

                                            {/* Improvements Section */}
                                            <div>
                                                <h5 className="font-semibold text-text mb-3 flex items-center gap-2">
                                                    <TrendingUp className="text-green-500" size={18} />
                                                    Suggested Improvements
                                                </h5>
                                                {audit.improvements && audit.improvements.length > 0 ? (
                                                    <ul className="space-y-2">
                                                        {audit.improvements.map((improvement, idx) => (
                                                            <li key={idx} className="flex items-start gap-2 text-sm">
                                                                <span className="text-green-500 mt-0.5">✓</span>
                                                                <span className="text-text-light">{improvement}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                ) : (
                                                    <p className="text-sm text-text-light italic">No improvement suggestions available.</p>
                                                )}
                                            </div>
                                        </div>

                                        {/* Validation Results if available */}
                                        {audit.validation_results && Object.keys(audit.validation_results).length > 0 && (
                                            <div className="mt-6 pt-6 border-t border-gray-200">
                                                <h5 className="font-semibold text-text mb-3">Validation Results</h5>
                                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                                    {Object.entries(audit.validation_results).map(([key, value]) => (
                                                        <div key={key} className="bg-white rounded-lg p-3 border border-gray-200">
                                                            <div className="text-xs text-text-light capitalize mb-1">
                                                                {key.replace(/_/g, ' ')}
                                                            </div>
                                                            <div className={`text-sm font-semibold ${value === true || value === 'PASS' ? 'text-green-600' : 'text-red-600'
                                                                }`}>
                                                                {typeof value === 'boolean' ? (value ? 'Pass' : 'Fail') : value}
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))
                    )}
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
