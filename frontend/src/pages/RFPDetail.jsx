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
  Download
} from 'lucide-react';
import { format } from 'date-fns';

const RFPDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [rfpData, setRfpData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [feedbackModalOpen, setFeedbackModalOpen] = useState(false);

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
      </div>
    );
  }

  const { rfp_summary, specifications, matches, pricing, recommended_sku } = rfpData;

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
        <button
          onClick={() => setFeedbackModalOpen(true)}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-light transition-colors"
        >
          Submit Feedback
        </button>
      </div>

      {/* RFP Summary */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-text">{rfp_summary.title}</h2>
            <p className="text-text-light mt-1">{rfp_summary.rfp_id}</p>
          </div>
          <StatusBadge status={rfp_summary.status} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <InfoItem label="Source" value={rfp_summary.source} />
          <InfoItem 
            label="Deadline" 
            value={format(new Date(rfp_summary.deadline), 'MMM dd, yyyy HH:mm')}
            icon={<Calendar size={16} />}
          />
          <InfoItem label="Discovered" value={format(new Date(rfp_summary.discovered_at), 'MMM dd, yyyy')} />
          {rfp_summary.match_score > 0 && (
            <InfoItem 
              label="Best Match Score" 
              value={`${(rfp_summary.match_score * 100).toFixed(0)}%`}
            />
          )}
        </div>
        <div className="mt-4">
          <h4 className="font-semibold text-text mb-2">Scope of Supply</h4>
          <p className="text-text-light">{rfp_summary.scope}</p>
        </div>
        {rfp_summary.testing_requirements.length > 0 && (
          <div className="mt-4">
            <h4 className="font-semibold text-text mb-2">Testing Requirements</h4>
            <div className="flex flex-wrap gap-2">
              {rfp_summary.testing_requirements.map((req, idx) => (
                <span key={idx} className="px-3 py-1 bg-primary/10 text-primary rounded-lg text-sm">
                  {req}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

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

      {/* Matched Products */}
      {matches && matches.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-xl font-bold text-text mb-4">Matched Products</h3>
          <div className="space-y-4">
            {matches.map((match, idx) => (
              <div 
                key={match.sku}
                className={`border-2 rounded-lg p-4 ${
                  match.sku === recommended_sku 
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
                  {Object.entries(match.specification_alignment).map(([key, value]) => (
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
                <a
                  href={match.datasheet_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-primary hover:text-primary-light text-sm"
                >
                  <ExternalLink size={14} />
                  View Datasheet
                </a>
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
    completed: 'bg-success/20 text-success'
  };

  return (
    <span className={`px-4 py-2 rounded-lg text-sm font-medium ${colors[status]}`}>
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
