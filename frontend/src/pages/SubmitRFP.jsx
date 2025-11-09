import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { rfpAPI } from '../services/api';
import { toast } from 'react-toastify';
import { Upload, Link as LinkIcon, FileText, CheckCircle, Loader } from 'lucide-react';
import { extractSpecifications, getSpecificationSummary, validateSpecifications } from '../utils/specExtractor';
import { matchProducts, getRecommendedProduct } from '../utils/productMatcher';
import { calculatePricing, formatCurrency } from '../utils/pricingCalculator';

const SubmitRFP = () => {
  const navigate = useNavigate();
  const [submissionType, setSubmissionType] = useState('url');
  const [formData, setFormData] = useState({
    title: '',
    source: '',
    deadline: '',
    scope: '',
    testing_requirements: ''
  });
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [processedData, setProcessedData] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.type !== 'application/pdf') {
        toast.error('Please select a PDF file');
        return;
      }
      setFile(selectedFile);
    }
  };

  // Auto-fill sample data for testing
  const fillSampleData = () => {
    setFormData({
      title: 'Supply of 11kV XLPE Aluminum Cables',
      source: 'https://example.com/tender-rfp-2025',
      deadline: '2025-12-15T17:00',
      scope: 'Supply of 5000 meters of 11kV XLPE cables with 3 core aluminum conductor, size 240 sq.mm. Cables should comply with IEC 60502-2 and IS 7098 standards. Armored with steel wire armor (SWA).',
      testing_requirements: 'Type test, Routine test, Partial discharge test'
    });
    toast.info('Sample data filled. You can now submit!');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setProcessing(true);

    try {
      const testingReqs = formData.testing_requirements
        .split(',')
        .map(r => r.trim())
        .filter(r => r);

      // Step 1: Extract specifications from scope
      toast.info('Extracting specifications...', { autoClose: 2000 });
      const specifications = extractSpecifications(formData.scope + ' ' + formData.title);
      
      if (specifications.length === 0) {
        toast.warning('No specifications detected. Please provide more details in the scope.');
        setSubmitting(false);
        setProcessing(false);
        return;
      }

      // Validate specifications
      const validation = validateSpecifications(specifications);
      if (!validation.isValid) {
        toast.warning(`Missing critical specifications: ${validation.missingFields.join(', ')}`);
      }

      // Get specification summary
      const specSummary = getSpecificationSummary(specifications);
      
      // Step 2: Match products
      toast.info('Matching products...', { autoClose: 2000 });
      const matches = matchProducts(specifications);
      
      if (matches.length === 0) {
        toast.warning('No matching products found. Try adjusting specifications.');
        setSubmitting(false);
        setProcessing(false);
        return;
      }

      // Step 3: Calculate pricing
      toast.info('Calculating pricing...', { autoClose: 2000 });
      
      // Extract quantity from specifications or use default
      const quantitySpec = specifications.find(s => s.type === 'quantity');
      const quantity = quantitySpec ? parseInt(quantitySpec.value) : 1000;
      
      const pricingList = calculatePricing(
        matches,
        quantity,
        formData.deadline,
        testingReqs
      );

      // Get recommended product
      const recommendedSku = getRecommendedProduct(matches, pricingList);
      const recommendedMatch = matches.find(m => m.sku === recommendedSku);
      const recommendedPricing = pricingList.find(p => p.sku === recommendedSku);

      // Store processed data
      const processed = {
        specifications,
        specSummary,
        matches,
        pricingList,
        recommendedSku,
        recommendedMatch,
        recommendedPricing,
        quantity
      };
      
      setProcessedData(processed);

      // Prepare RFP data with processing results
      const rfpData = {
        title: formData.title,
        source: submissionType === 'url' ? formData.source : `File: ${file?.name || 'uploaded'}`,
        deadline: new Date(formData.deadline).toISOString(),
        scope: formData.scope,
        testing_requirements: testingReqs,
        // Add processed results
        match_score: recommendedMatch?.match_score || 0,
        total_estimate: recommendedPricing?.total || 0,
        status: 'completed',
        specifications: specSummary,
        matched_products: matches.length,
        recommended_sku: recommendedSku
      };

      const response = await rfpAPI.submitRFP(rfpData);
      
      setProcessing(false);
      toast.success('RFP processed successfully!', { autoClose: 3000 });
      
      // Show results for 3 seconds before redirecting
      setTimeout(() => {
        navigate(`/rfp/${response.data.rfp_id}`);
      }, 3000);
    } catch (error) {
      console.error('Error submitting RFP:', error);
      toast.error('Failed to process RFP. Please try again.');
      setProcessing(false);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h2 className="text-3xl font-bold text-text">Submit New RFP</h2>
          <p className="text-text-light mt-1">Add a new RFP for automated processing</p>
        </div>
        <button
          onClick={fillSampleData}
          className="px-4 py-2 text-sm bg-gray-100 text-text rounded-lg hover:bg-gray-200 transition-colors"
        >
          Fill Sample Data
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        {/* Submission Type Selector */}
        <div className="flex gap-4 mb-6">
          <button
            type="button"
            onClick={() => setSubmissionType('url')}
            className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-colors ${
              submissionType === 'url'
                ? 'border-primary bg-primary text-white'
                : 'border-gray-300 text-text hover:border-primary'
            }`}
          >
            <LinkIcon size={20} />
            <span>From URL</span>
          </button>
          <button
            type="button"
            onClick={() => setSubmissionType('file')}
            className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-colors ${
              submissionType === 'file'
                ? 'border-primary bg-primary text-white'
                : 'border-gray-300 text-text hover:border-primary'
            }`}
          >
            <Upload size={20} />
            <span>Upload PDF</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* URL Input */}
          {submissionType === 'url' && (
            <div>
              <label className="block text-sm font-medium text-text mb-2">
                RFP Source URL <span className="text-error">*</span>
              </label>
              <input
                type="url"
                name="source"
                value={formData.source}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://example.com/rfp-document.pdf"
              />
            </div>
          )}

          {/* File Upload */}
          {submissionType === 'file' && (
            <div>
              <label className="block text-sm font-medium text-text mb-2">
                Upload RFP Document (PDF) <span className="text-error">*</span>
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  className="hidden"
                  id="file-upload"
                  required
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <FileText size={48} className="mx-auto text-text-light mb-2" />
                  {file ? (
                    <p className="text-text font-medium">{file.name}</p>
                  ) : (
                    <>
                      <p className="text-text font-medium">Click to upload PDF</p>
                      <p className="text-text-light text-sm mt-1">or drag and drop</p>
                    </>
                  )}
                </label>
              </div>
            </div>
          )}

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              RFP Title <span className="text-error">*</span>
            </label>
            <input
              type="text"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="e.g., Supply of 11kV XLPE Cables"
            />
          </div>

          {/* Deadline */}
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Submission Deadline <span className="text-error">*</span>
            </label>
            <input
              type="datetime-local"
              name="deadline"
              value={formData.deadline}
              onChange={handleInputChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {/* Scope */}
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Scope of Supply <span className="text-error">*</span>
            </label>
            <textarea
              name="scope"
              value={formData.scope}
              onChange={handleInputChange}
              required
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Describe the scope of supply in detail..."
            />
          </div>

          {/* Testing Requirements */}
          <div>
            <label className="block text-sm font-medium text-text mb-2">
              Testing Requirements
            </label>
            <input
              type="text"
              name="testing_requirements"
              value={formData.testing_requirements}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="e.g., IEC 60502, Type test, Routine test (comma-separated)"
            />
            <p className="text-sm text-text-light mt-1">
              Enter testing requirements separated by commas
            </p>
          </div>

          {/* Submit Button */}
          <div className="flex gap-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="flex-1 px-6 py-3 border border-gray-300 text-text rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary-light transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                  Submitting...
                </span>
              ) : (
                'Submit RFP'
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Info Box */}
      <div className="bg-primary/10 border border-primary/30 rounded-lg p-4">
        <h4 className="font-semibold text-primary mb-2">What happens next?</h4>
        <ul className="text-sm text-text space-y-1">
          <li>• System will parse the RFP document and extract specifications</li>
          <li>• Product matching engine will find best-fit products from catalog</li>
          <li>• Pricing calculator will generate cost estimates</li>
          <li>• Complete response will be available immediately</li>
        </ul>
      </div>

      {/* Processing Results */}
      {processing && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center gap-3 mb-4">
            <Loader className="animate-spin text-primary" size={24} />
            <h3 className="text-xl font-bold text-text">Processing RFP...</h3>
          </div>
          <div className="space-y-2 text-text-light">
            <p>✓ Extracting specifications from scope</p>
            <p>✓ Matching products from catalog</p>
            <p>✓ Calculating pricing estimates</p>
          </div>
        </div>
      )}

      {/* Processed Results Display */}
      {processedData && !processing && (
        <div className="space-y-6">
          {/* Specifications Found */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="text-success" size={24} />
              <h3 className="text-xl font-bold text-text">Specifications Extracted</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {processedData.specifications.map((spec, idx) => (
                <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <span className="text-text-light capitalize">{spec.type.replace(/_/g, ' ')}</span>
                  <span className="font-semibold text-text">
                    {spec.value} {spec.unit}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Product Matches */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="text-success" size={24} />
              <h3 className="text-xl font-bold text-text">
                {processedData.matches.length} Products Matched
              </h3>
            </div>
            <div className="space-y-3">
              {processedData.matches.slice(0, 3).map((match) => (
                <div key={match.sku} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="font-semibold text-text">{match.name}</h4>
                      <p className="text-sm text-text-light">{match.sku}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      match.match_score >= 0.9 ? 'bg-success/20 text-success' :
                      match.match_score >= 0.7 ? 'bg-warning/20 text-warning' :
                      'bg-gray-200 text-text'
                    }`}>
                      {(match.match_score * 100).toFixed(0)}% Match
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2">
                    {match.matched_specs.map((spec, idx) => (
                      <span key={idx} className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">
                        {spec.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pricing Estimate */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle className="text-success" size={24} />
              <h3 className="text-xl font-bold text-text">Pricing Calculated</h3>
            </div>
            
            {/* Recommended Option */}
            {processedData.recommendedPricing && (
              <div className="p-4 bg-primary/10 border-2 border-primary rounded-lg mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-primary">RECOMMENDED</span>
                  <span className="text-2xl font-bold text-primary">
                    {formatCurrency(processedData.recommendedPricing.total)}
                  </span>
                </div>
                <p className="text-text font-semibold mb-3">{processedData.recommendedMatch.name}</p>
                <div className="grid grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="text-text-light">Unit Price:</span>
                    <span className="ml-2 text-text font-medium">
                      ₹{processedData.recommendedPricing.unit_price}/m
                    </span>
                  </div>
                  <div>
                    <span className="text-text-light">Quantity:</span>
                    <span className="ml-2 text-text font-medium">
                      {processedData.quantity}m
                    </span>
                  </div>
                  <div>
                    <span className="text-text-light">Material:</span>
                    <span className="ml-2 text-text font-medium">
                      {formatCurrency(processedData.recommendedPricing.subtotal)}
                    </span>
                  </div>
                  <div>
                    <span className="text-text-light">Testing:</span>
                    <span className="ml-2 text-text font-medium">
                      {formatCurrency(processedData.recommendedPricing.testing_cost)}
                    </span>
                  </div>
                  <div>
                    <span className="text-text-light">Delivery:</span>
                    <span className="ml-2 text-text font-medium">
                      {formatCurrency(processedData.recommendedPricing.delivery_cost)}
                    </span>
                  </div>
                  {processedData.recommendedPricing.urgency_adjustment > 0 && (
                    <div>
                      <span className="text-text-light">Urgency:</span>
                      <span className="ml-2 text-error font-medium">
                        +{formatCurrency(processedData.recommendedPricing.urgency_adjustment)}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Other Options */}
            {processedData.pricingList.length > 1 && (
              <div>
                <h4 className="font-semibold text-text mb-3">Alternative Options</h4>
                <div className="space-y-2">
                  {processedData.pricingList
                    .filter(p => p.sku !== processedData.recommendedSku)
                    .slice(0, 2)
                    .map((pricing) => (
                      <div key={pricing.sku} className="flex justify-between items-center p-3 border border-gray-200 rounded">
                        <div>
                          <p className="font-medium text-text">{pricing.product_name}</p>
                          <p className="text-sm text-text-light">{pricing.sku}</p>
                        </div>
                        <span className="text-lg font-bold text-text">
                          {formatCurrency(pricing.total)}
                        </span>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>

          {/* Success Message */}
          <div className="bg-success/10 border border-success/30 rounded-lg p-4 text-center">
            <p className="text-success font-semibold">
              ✓ RFP processing complete! Redirecting to details...
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SubmitRFP;
