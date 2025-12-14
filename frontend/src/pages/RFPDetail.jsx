import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { rfpAPI } from '../services/api';
import { toast } from 'react-toastify';
import {
  ArrowLeft,
  Calendar,
  ExternalLink,
  CheckCircle,
  AlertTriangle,
  Download,
  FileText,
  X,
  XCircle,
  Lightbulb
} from 'lucide-react';
import { format } from 'date-fns';

const RFPDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [rfpData, setRfpData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedbackModalOpen, setFeedbackModalOpen] = useState(false);
  const [proposalPdfOpen, setProposalPdfOpen] = useState(false);
  const [proposalPdfUrl, setProposalPdfUrl] = useState('');

  useEffect(() => {
    loadRFPDetail();
  }, [id]);

  const loadRFPDetail = async () => {
    try {
      const response = await rfpAPI.getRFP(id);
      setRfpData(response.data);
    } catch (error) {
      console.error('Error loading RFP details:', error);
      toast.error('Failed to load RFP details');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePDF = async () => {
    try {
      toast.info('Generating PDF...');
      const response = await rfpAPI.generateProposalPDF(id);

      // Determine URL based on response
      let url;
      if (response.data && response.data.download_url) {
        // Build absolute URL if relative
        url = response.data.download_url.startsWith('http')
          ? response.data.download_url
          : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${response.data.download_url}`;
      } else {
        // Fallback or error
        throw new Error('No download URL returned');
      }

      setProposalPdfUrl(url);
      setProposalPdfOpen(true);
      toast.success('PDF generated successfully');
    } catch (error) {
      console.error('Error generating PDF:', error);
      toast.error('Failed to generate PDF');
    }
  };

  const handleGenerateDoc = async () => {
    try {
      toast.info('Generating Word Document...');
      const response = await rfpAPI.generateProposalDoc(id);

      if (response.data && response.data.download_url) {
        const url = response.data.download_url.startsWith('http')
          ? response.data.download_url
          : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}${response.data.download_url}`;

        // Trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = `proposal_${id}.doc`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        toast.success('Word document downloaded');
      }
    } catch (error) {
      console.error('Error generating Doc:', error);
      toast.error('Failed to generate Word document');
    }
  };

  const handleFeedbackSubmit = async (feedback) => {
    try {
      await rfpAPI.submitFeedback(id, feedback);
      toast.success('Feedback submitted successfully');
      setFeedbackModalOpen(false);
    } catch (error) {
      toast.error('Failed to submit feedback');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!rfpData) {
    return (
      <div className="text-center py-12">
        <p className="text-text-light">RFP not found</p>
        <button
          onClick={() => navigate('/rfps')}
          className="mt-4 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-light"
        >
          Back to List
        </button>
      </div>
    );
  }

  // Handle flat data structure
  const {
    rfp_id, title, source, deadline, scope, status, discovered_at,
    match_score, testing_requirements, specifications, matches, pricing, recommended_sku
  } = rfpData;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="flex items-center gap-2 text-primary hover:text-primary-light"
        >
          <ArrowLeft size={20} />
          <span>Back to List</span>
        </button>
        <div className="flex items-center gap-3">
          {rfpData?.status === 'completed' && (
            <>
              <button
                onClick={handleGenerateDoc}
                className="px-4 py-2 bg-olive-600 text-white rounded-lg hover:bg-olive-700 transition-colors flex items-center gap-2"
                title="Download as Word Doc"
              >
                <FileText size={18} />
                Download DOC
              </button>
              <button
                onClick={handleGeneratePDF}
                className="px-4 py-2 bg-olive-600 text-white rounded-lg hover:bg-olive-700 transition-colors flex items-center gap-2"
              >
                <Download size={18} />
                Generate PDF
              </button>
            </>
          )}
          <button
            onClick={() => setFeedbackModalOpen(true)}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-light transition-colors"
          >
            Submit Feedback
          </button>
        </div>
      </div>

      {/* RFP Summary */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-text">{title || 'Untitled RFP'}</h2>
            <p className="text-text-light mt-1">{rfp_id}</p>
          </div>
          <StatusBadge status={status || 'new'} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <InfoItem label="Source" value={source || 'Unknown'} />
          <InfoItem
            label="Deadline"
            value={deadline ? format(new Date(deadline), 'MMM dd, yyyy HH:mm') : 'N/A'}
            icon={<Calendar size={16} />}
          />
          <InfoItem label="Discovered" value={discovered_at ? format(new Date(discovered_at), 'MMM dd, yyyy') : 'N/A'} />
          {match_score > 0 && (
            <InfoItem
              label="Best Match Score"
              value={`${(match_score * 100).toFixed(0)}%`}
            />
          )}
        </div>
        <div className="mt-4">
          <h4 className="font-semibold text-text mb-2">Scope of Supply</h4>
          <p className="text-text-light">{scope || 'No scope defined'}</p>
        </div>
        {testing_requirements && testing_requirements.length > 0 && (
          <div className="mt-4">
            <h4 className="font-semibold text-text mb-2">Testing Requirements</h4>
            <div className="flex flex-wrap gap-2">
              {testing_requirements.map((req, idx) => (
                <span key={idx} className="px-3 py-1 bg-primary/10 text-primary rounded-lg text-sm">
                  {req}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Failure Analysis */}
      {status === 'failed' && specifications?.failure_reason && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 shadow-sm">
          <h3 className="text-xl font-bold text-red-800 mb-4 flex items-center gap-2">
            <XCircle className="text-red-600" />
            Failure Analysis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg border border-red-100 shadow-sm">
              <p className="text-xs font-bold text-red-600 uppercase tracking-wide mb-2">Root Cause</p>
              <p className="text-gray-800 font-medium">{specifications.failure_reason}</p>
            </div>
            {specifications.improvement_advice && (
              <div className="bg-white p-4 rounded-lg border border-amber-100 shadow-sm">
                <p className="text-xs font-bold text-amber-600 uppercase tracking-wide mb-2 flex items-center gap-1">
                  <Lightbulb size={14} />
                  Strategy & Advice
                </p>
                <p className="text-gray-800 font-medium">{specifications.improvement_advice}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Specifications */}
      {specifications && Object.keys(specifications).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-text mb-4">Technical Specifications</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(specifications).map(([key, value]) => (
              <div key={key} className="border border-gray-200 rounded-lg p-4">
                <p className="text-sm text-text-light mb-1">
                  {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </p>
                <p className="font-semibold text-text">
                  {Array.isArray(value) ? value.join(', ') : value}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Audit Report */}
      {rfpData?.audit_report && Object.keys(rfpData.audit_report).length > 0 && (
        <div className={`rounded-lg shadow-md p-6 ${
          rfpData.audit_report.is_compliant 
            ? 'bg-green-50 border-2 border-green-200' 
            : rfpData.audit_report.recommendation === 'REJECT' 
            ? 'bg-red-50 border-2 border-red-200' 
            : 'bg-yellow-50 border-2 border-yellow-200'
        }`}>
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-xl font-bold text-text mb-2 flex items-center gap-2">
                {rfpData.audit_report.is_compliant ? (
                  <CheckCircle className="text-green-600" size={24} />
                ) : (
                  <AlertTriangle className="text-amber-600" size={24} />
                )}
                Audit Report
              </h3>
              <p className="text-sm text-text-light">
                Validated at: {rfpData.audit_report.validated_at ? format(new Date(rfpData.audit_report.validated_at), 'MMM dd, yyyy HH:mm') : 'N/A'}
              </p>
            </div>
            <div className="text-right">
              <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg font-bold ${
                rfpData.audit_report.recommendation === 'APPROVE' 
                  ? 'bg-green-600 text-white' 
                  : rfpData.audit_report.recommendation === 'REJECT' 
                  ? 'bg-red-600 text-white' 
                  : 'bg-yellow-600 text-white'
              }`}>
                {rfpData.audit_report.recommendation}
              </div>
              <p className="text-sm text-text-light mt-2">
                Compliance Score: <span className="font-bold">{(rfpData.audit_report.compliance_score * 100).toFixed(0)}%</span>
              </p>
            </div>
          </div>

          {/* Issues */}
          {rfpData.audit_report.issues && rfpData.audit_report.issues.length > 0 && (
            <div className="bg-white rounded-lg p-4 mb-4 border-l-4 border-red-500">
              <h4 className="font-bold text-red-700 mb-2 flex items-center gap-2">
                <XCircle size={18} />
                Critical Issues ({rfpData.audit_report.issues.length})
              </h4>
              <ul className="list-disc list-inside space-y-1">
                {rfpData.audit_report.issues.map((issue, idx) => (
                  <li key={idx} className="text-red-800 text-sm">{issue}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Warnings */}
          {rfpData.audit_report.warnings && rfpData.audit_report.warnings.length > 0 && (
            <div className="bg-white rounded-lg p-4 mb-4 border-l-4 border-yellow-500">
              <h4 className="font-bold text-yellow-700 mb-2 flex items-center gap-2">
                <AlertTriangle size={18} />
                Warnings ({rfpData.audit_report.warnings.length})
              </h4>
              <ul className="list-disc list-inside space-y-1">
                {rfpData.audit_report.warnings.map((warning, idx) => (
                  <li key={idx} className="text-yellow-800 text-sm">{warning}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Compliance Checks */}
          {rfpData.audit_report.checks && Object.keys(rfpData.audit_report.checks).length > 0 && (
            <div className="bg-white rounded-lg p-4">
              <h4 className="font-bold text-text mb-3">Compliance Checks</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {Object.entries(rfpData.audit_report.checks).map(([checkName, checkResult]) => (
                  <div key={checkName} className={`flex items-center gap-2 p-3 rounded-lg ${
                    checkResult.passed ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {checkResult.passed ? (
                      <CheckCircle className="text-green-600" size={20} />
                    ) : (
                      <XCircle className="text-red-600" size={20} />
                    )}
                    <div className="flex-1">
                      <p className="font-semibold text-sm">
                        {checkName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </p>
                      {checkResult.message && (
                        <p className="text-xs text-text-light">{checkResult.message}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Match and Pricing Validation */}
          {rfpData.audit_report.matches_validation && (
            <div className="bg-white rounded-lg p-4 mt-4">
              <h4 className="font-bold text-text mb-2">Product Match Validation</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="text-center">
                  <p className="text-xs text-text-light">Best Match</p>
                  <p className="text-lg font-bold text-primary">
                    {(rfpData.audit_report.matches_validation.best_match_score * 100).toFixed(0)}%
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-text-light">Average</p>
                  <p className="text-lg font-bold">
                    {(rfpData.audit_report.matches_validation.average_match_score * 100).toFixed(0)}%
                  </p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-text-light">Matches</p>
                  <p className="text-lg font-bold">{rfpData.audit_report.matches_validation.match_count}</p>
                </div>
                <div className="text-center">
                  <p className="text-xs text-text-light">Quality</p>
                  <p className={`text-lg font-bold ${
                    rfpData.audit_report.matches_validation.recommendation === 'GOOD' 
                      ? 'text-green-600' 
                      : rfpData.audit_report.matches_validation.recommendation === 'ACCEPTABLE' 
                      ? 'text-yellow-600' 
                      : 'text-red-600'
                  }`}>
                    {rfpData.audit_report.matches_validation.recommendation}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Matched Products */}
      {matches && matches.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-text mb-4">Matched Products</h3>
          <div className="space-y-4">
            {matches.map((match) => (
              <div
                key={match.sku}
                className={`border-2 rounded-lg p-4 ${match.sku === recommended_sku
                  ? 'border-success bg-success/5'
                  : 'border-gray-200'
                  }`}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-text">{match.product_name}</h4>
                      {match.sku === recommended_sku && (
                        <span className="px-2 py-1 bg-success text-white text-xs rounded-full">
                          Recommended
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-text-light">SKU: {match.sku}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-text-light">Match Score</p>
                    <p className="text-2xl font-bold text-primary">
                      {(match.match_score * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                  {match.specification_alignment && Object.entries(match.specification_alignment).map(([key, value]) => (
                    <div key={key} className="flex items-center gap-2">
                      {value === 'exact_match' ? (
                        <CheckCircle size={16} className="text-success" />
                      ) : (
                        <AlertTriangle size={16} className="text-warning" />
                      )}
                      <div>
                        <p className="text-xs text-text-light">
                          {key.replace(/_/g, ' ')}
                        </p>
                        <p className="text-xs font-medium">
                          {value.replace(/_/g, ' ')}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                {match.datasheet_url && (
                  <a
                    href={match.datasheet_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-primary hover:text-primary-light text-sm"
                  >
                    <ExternalLink size={14} />
                    View Datasheet
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Pricing Breakdown */}
      {pricing && pricing.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-text mb-4">Pricing Breakdown</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-sm font-semibold text-text">Product</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Unit Price</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Quantity</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Subtotal</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Testing</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Delivery</th>
                  <th className="px-4 py-3 text-right text-sm font-semibold text-text">Total</th>
                </tr>
              </thead>
              <tbody>
                {pricing.map((item) => (
                  <tr
                    key={item.sku}
                    className={item.sku === recommended_sku ? 'bg-success/5' : ''}
                  >
                    <td className="px-4 py-3 text-sm">
                      {item.sku}
                      {item.sku === recommended_sku && (
                        <span className="ml-2 text-xs text-success">★ Recommended</span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-right">₹{item.unit_price.toFixed(2)}</td>
                    <td className="px-4 py-3 text-sm text-right">{item.quantity}</td>
                    <td className="px-4 py-3 text-sm text-right">₹{item.subtotal.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">₹{item.testing_cost.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right">₹{item.delivery_cost.toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm text-right font-semibold">
                      ₹{item.total.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Proposal PDF Modal */}
      {proposalPdfOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-2xl w-full max-w-5xl h-[90vh] flex flex-col">
            {/* Header with Download Icon */}
            <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-green-50 to-green-100">
              <div>
                <h3 className="text-lg font-bold text-gray-800">Business Proposal</h3>
                <p className="text-sm text-gray-600">RFP #{rfp_id} - {title}</p>
              </div>
              <div className="flex items-center gap-2">
                {/* Download Icon Button */}
                <a
                  href={proposalPdfUrl}
                  download={`Proposal_${rfp_id}.pdf`}
                  className="p-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
                  title="Download PDF"
                >
                  <Download size={20} />
                </a>
                {/* Close Button */}
                <button
                  onClick={() => setProposalPdfOpen(false)}
                  className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  <X size={20} />
                </button>
              </div>
            </div>

            {/* PDF Iframe */}
            <div className="flex-1 p-4 bg-gray-50">
              <iframe
                src={proposalPdfUrl}
                className="w-full h-full border-0 rounded shadow-inner"
                title="Proposal PDF"
              />
            </div>

            {/* Footer with Send Mail Button */}
            <div className="p-4 border-t bg-white flex justify-between items-center">
              <button
                onClick={() => setProposalPdfOpen(false)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Close
              </button>

              {/* Send Mail Button */}
              <a
                href={`https://mail.google.com/mail/?view=cm&fs=1&to=${encodeURIComponent(
                  'pamedipagaraphel@gmail.com'
                )}&su=${encodeURIComponent(
                  `Business Proposal for RFP #${rfp_id} - ${title || 'RFP Submission'}`
                )}&body=${encodeURIComponent(
                  `Dear Sir/Madam,\n\nPlease find attached our comprehensive business proposal for RFP #${rfp_id}.\n\nRFP Title: ${title}\nProposed Amount: ₹${rfpData.total_estimate?.toFixed(2) || 'N/A'}\n\nWe look forward to your positive response.\n\nBest Regards,\nComet Student Benefits\n\n(Note: This draft has been auto-generated. Please ensure the downloaded Proposal PDF is attached before sending.)`
                )}`}
                target="_blank"
                rel="noopener noreferrer"
                className="px-6 py-3 bg-olive-600 text-white rounded-lg hover:bg-olive-700 transition-all shadow-md flex items-center gap-2 font-medium"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                </svg>
                Send via Gmail
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Feedback Modal */}
      {feedbackModalOpen && (
        <FeedbackModal
          onClose={() => setFeedbackModalOpen(false)}
          onSubmit={handleFeedbackSubmit}
        />
      )}
    </div>
  );
};

const InfoItem = ({ label, value, icon }) => (
  <div>
    <p className="text-sm text-text-light mb-1">{label}</p>
    <div className="flex items-center gap-2">
      {icon}
      <p className="font-medium text-text">{value}</p>
    </div>
  </div>
);

const StatusBadge = ({ status }) => {
  const colors = {
    new: 'bg-blue-100 text-blue-800',
    processing: 'bg-warning/20 text-warning',
    auditing: 'bg-purple-100 text-purple-800',
    completed: 'bg-success/20 text-success',
    failed: 'bg-red-100 text-red-800'
  };

  const icons = {
    new: '🆕',
    processing: '⚙️',
    auditing: '🔍',
    completed: '✅',
    failed: '❌'
  };

  return (
    <span className={`px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2 ${colors[status] || 'bg-gray-100 text-gray-800'}`}>
      <span>{icons[status] || '📄'}</span>
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

const FeedbackModal = ({ onClose, onSubmit }) => {
  const [outcome, setOutcome] = useState('won');
  const [actualPrice, setActualPrice] = useState('');
  const [notes, setNotes] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      outcome,
      actual_price: parseFloat(actualPrice) || 0,
      notes
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 className="text-xl font-bold text-text mb-4">Submit RFP Feedback</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Outcome
            </label>
            <select
              value={outcome}
              onChange={(e) => setOutcome(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="won">Won</option>
              <option value="lost">Lost</option>
              <option value="pending">Pending</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Actual Price (₹)
            </label>
            <input
              type="number"
              value={actualPrice}
              onChange={(e) => setActualPrice(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter actual price"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Notes
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Additional notes..."
            />
          </div>
          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-text rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-light"
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RFPDetail;
