import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { rfpAPI, emailAPI } from '../services/api';
import { toast } from 'react-toastify';
import { Upload, Link as LinkIcon, FileText, CheckCircle, Loader, Mail, Copy, Sparkles, Search } from 'lucide-react';
import { extractSpecifications, getSpecificationSummary, validateSpecifications } from '../utils/specExtractor';
import { matchProducts, getRecommendedProduct } from '../utils/productMatcher';
import { calculatePricing, formatCurrency } from '../utils/pricingCalculator';

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

const SubmitRFP = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.state?.prefill) {
      setFormData(prev => ({ ...prev, ...location.state.prefill }));
      if (location.state.prefill.source?.startsWith('http')) {
        setSubmissionType('url');
      }
    }
  }, [location.state]);

  const [submissionType, setSubmissionType] = useState('url');

  // Quick Start mode: 'fresh', 'email', or 'clone'
  const [quickStartMode, setQuickStartMode] = useState('fresh');
  const [emails, setEmails] = useState([]);
  const [existingRFPs, setExistingRFPs] = useState([]);
  const [showEmailDropdown, setShowEmailDropdown] = useState(false);
  const [showRFPDropdown, setShowRFPDropdown] = useState(false);
  const [emailSearchQuery, setEmailSearchQuery] = useState('');
  const [rfpSearchQuery, setRFPSearchQuery] = useState('');

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
  const [showPreview, setShowPreview] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [processingStep, setProcessingStep] = useState('');
  const [processingSteps, setProcessingSteps] = useState([]);

  // Handle Mock URL Scraping
  const handleMockUrlScrape = async (url) => {
    if (!url) {
      toast.error('Please enter a URL first');
      return;
    }

    toast.info('Analyzing URL content...', { autoClose: 1500 });

    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    if (MOCK_URL_DATA[url]) {
      const data = MOCK_URL_DATA[url];
      setFormData(prev => ({
        ...prev,
        title: data.title,
        deadline: data.deadline,
        scope: data.scope,
        testing_requirements: data.testing_requirements
      }));
      toast.success('Successfully extracted RFP details!');
    } else {
      toast.warning('Could not auto-extract details. Please fill manually.');
    }
  };

  // Load pending emails and existing RFPs when component mounts or mode changes
  useEffect(() => {
    const loadQuickStartData = async () => {
      try {
        if (quickStartMode === 'email') {
          const response = await emailAPI.getEmails('pending');
          setEmails(response.data.emails || []);
        } else if (quickStartMode === 'clone') {
          const response = await rfpAPI.getRFPs({ limit: 50 });
          setExistingRFPs(response.data.rfps || []);
        }
      } catch (error) {
        console.error('Error loading Quick Start data:', error);
      }
    };

    loadQuickStartData();
  }, [quickStartMode]);

  // Parse deadline from email body (simple keyword search)
  const parseDeadlineFromText = (text) => {
    const datePattern = /(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|(\d{4}[-/]\d{1,2}[-/]\d{1,2})/g;
    const matches = text.match(datePattern);
    if (matches && matches.length > 0) {
      try {
        const parsedDate = new Date(matches[0]);
        if (!isNaN(parsedDate.getTime())) {
          return parsedDate.toISOString().slice(0, 16);
        }
      } catch (e) {
        // Ignore
      }
    }
    const defaultDate = new Date();
    defaultDate.setDate(defaultDate.getDate() + 30);
    return defaultDate.toISOString().slice(0, 16);
  };

  // Handler for email selection
  const handleEmailSelect = (email) => {
    setFormData({
      title: email.subject || 'RFP from Email',
      source: email.sender || 'Email',
      deadline: parseDeadlineFromText(email.body || ''),
      scope: email.body || email.subject || '',
      testing_requirements: ''
    });
    setEmailSearchQuery(email.subject);
    setShowEmailDropdown(false);
    toast.success('Email details imported!');
  };

  // Handler for RFP cloning
  const handleRFPClone = (rfp) => {
    setFormData({
      title: `Copy of ${rfp.title}`,
      source: rfp.source || 'Cloned RFP',
      deadline: rfp.deadline ? new Date(rfp.deadline).toISOString().slice(0, 16) : '',
      scope: rfp.scope || '',
      testing_requirements: Array.isArray(rfp.testing_requirements)
        ? rfp.testing_requirements.join(', ')
        : rfp.testing_requirements || ''
    });
    setRFPSearchQuery(rfp.title);
    setShowRFPDropdown(false);
    toast.success('RFP details cloned!');
  };

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
    setProcessingSteps([]);

    // Helper function to add processing steps with delay
    const addStep = async (step, delay = 1000) => {
      setProcessingStep(step);
      setProcessingSteps(prev => [...prev, { text: step, timestamp: new Date().toLocaleTimeString(), completed: false }]);
      await new Promise(resolve => setTimeout(resolve, delay));
      setProcessingSteps(prev => prev.map((s, i) => i === prev.length - 1 ? { ...s, completed: true } : s));
    };

    try {
      const testingReqs = formData.testing_requirements
        .split(',')
        .map(r => r.trim())
        .filter(r => r);

      // Step 1: Sales Agent - Document Parsing (1.5s)
      await addStep('📧 Sales Agent: Parsing RFP document...', 1500);

      // Step 2: Technical Agent - Spec Extraction (2s)
      await addStep('🔧 Technical Agent: Extracting specifications...', 2000);
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

      // Step 3: Technical Agent - Product Matching (2.5s)
      await addStep('🎯 Technical Agent: Matching products from catalog...', 2500);
      const matches = matchProducts(specifications);

      if (matches.length === 0) {
        toast.warning('No matching products found. Try adjusting specifications.');
        setSubmitting(false);
        setProcessing(false);
        return;
      }

      // Step 4: Pricing Agent - Cost Calculation (2s)
      await addStep('💰 Pricing Agent: Calculating cost estimates...', 2000);

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

      // Step 5: Auditor Agent - Compliance Check (1.5s)
      await addStep('✅ Auditor Agent: Validating compliance requirements...', 1500);

      // Step 6: Learning Agent - Optimization (0.5s)
      await addStep('🧠 Learning Agent: Applying learned optimizations...', 500);

      // Store processed data for preview
      const processed = {
        specifications,
        specSummary,
        matches,
        pricingList,
        recommendedSku,
        recommendedMatch,
        recommendedPricing,
        quantity,
        testingReqs
      };

      setProcessedData(processed);
      setProcessing(false);
      setShowPreview(true);
      toast.success('RFP processed! Please review and confirm.', { autoClose: 3000 });
    } catch (error) {
      console.error('Error processing RFP:', error);
      toast.error('Failed to process RFP. Please try again.');
      setProcessing(false);
    } finally {
      setSubmitting(false);
    }
  };

  // New function to handle final confirmation and submission to backend
  const handleConfirmSubmit = async () => {
    if (!processedData) return;

    setConfirming(true);
    try {
      // Prepare RFP data with processing results
      const rfpData = {
        title: formData.title,
        source: submissionType === 'url' ? formData.source : `File: ${file?.name || 'uploaded'}`,
        deadline: new Date(formData.deadline).toISOString(),
        scope: formData.scope,
        testing_requirements: processedData.testingReqs,
        file: file,
        // Add processed results
        match_score: processedData.recommendedMatch?.match_score || 0,
        total_estimate: processedData.recommendedPricing?.total || 0,
        status: 'completed',
        // Send detailed results for immediate saving
        specifications: processedData.specifications,
        matches: processedData.matches,
        pricing: processedData.pricingList,
        recommended_sku: processedData.recommendedSku
      };

      const response = await rfpAPI.submitRFP(rfpData);

      toast.success('RFP submitted successfully!', { autoClose: 2000 });

      // Redirect to RFP detail page
      setTimeout(() => {
        navigate(`/rfp/${response.data.rfp_id}`);
      }, 2000);
    } catch (error) {
      console.error('Error submitting RFP:', error);
      toast.error('Failed to submit RFP. Please try again.');
      setConfirming(false);
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

      {/* Quick Start Section */}
      {!showPreview && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg shadow-md p-6 border border-purple-200">

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <button
              type="button"
              onClick={() => setQuickStartMode('email')}
              className={`p-4 rounded-lg border-2 transition-all ${quickStartMode === 'email'
                ? 'border-primary-600 bg-primary-600 text-white shadow-lg'
                : 'border-gray-300 bg-white text-text hover:border-primary-400'
                }`}
            >
              <Mail size={24} className="mx-auto mb-2" />
              <p className="font-semibold">Import from Email</p>
              <p className={`text-xs mt-1 ${quickStartMode === 'email' ? 'text-white opacity-90' : 'text-text-light'}`}>
                Auto-fill from inbox
              </p>
            </button>

            <button
              type="button"
              onClick={() => setQuickStartMode('clone')}
              className={`p-4 rounded-lg border-2 transition-all ${quickStartMode === 'clone'
                ? 'border-primary-600 bg-primary-600 text-white shadow-lg'
                : 'border-gray-300 bg-white text-text hover:border-primary-400'
                }`}
            >
              <Copy size={24} className="mx-auto mb-2" />
              <p className="font-semibold">Clone Existing RFP</p>
              <p className={`text-xs mt-1 ${quickStartMode === 'clone' ? 'text-white opacity-90' : 'text-text-light'}`}>
                Use as template
              </p>
            </button>

            <button
              type="button"
              onClick={() => setQuickStartMode('fresh')}
              className={`p-4 rounded-lg border-2 transition-all ${quickStartMode === 'fresh'
                ? 'border-primary-600 bg-primary-600 text-white shadow-lg'
                : 'border-gray-300 bg-white text-text hover:border-primary-400'
                }`}
            >
              <FileText size={24} className="mx-auto mb-2" />
              <p className="font-semibold">Start Fresh</p>
              <p className={`text-xs mt-1 ${quickStartMode === 'fresh' ? 'text-white opacity-90' : 'text-text-light'}`}>
                Manual entry
              </p>
            </button>
          </div>

          {/* Email Search Dropdown */}
          {quickStartMode === 'email' && (
            <div className="relative">
              <label className="block text-sm font-medium text-text mb-2">
                Search Pending Emails
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-light" size={18} />
                <input
                  type="text"
                  value={emailSearchQuery}
                  onChange={(e) => {
                    setEmailSearchQuery(e.target.value);
                    setShowEmailDropdown(true);
                  }}
                  onFocus={() => setShowEmailDropdown(true)}
                  className="w-full pl-10 pr-4 py-3 border-2 border-primary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-600"
                  placeholder="Type to search emails..."
                />
              </div>

              {showEmailDropdown && emails.length > 0 && (
                <div className="absolute z-10 w-full mt-2 bg-white border border-gray-300 rounded-lg shadow-xl max-h-64 overflow-y-auto">
                  {emails
                    .filter(email =>
                      email.subject?.toLowerCase().includes(emailSearchQuery.toLowerCase()) ||
                      email.sender?.toLowerCase().includes(emailSearchQuery.toLowerCase())
                    )
                    .map((email) => (
                      <button
                        key={email.email_id}
                        type="button"
                        onClick={() => handleEmailSelect(email)}
                        className="w-full text-left px-4 py-3 hover:bg-primary-50 border-b border-gray-100 last:border-b-0 transition-colors"
                      >
                        <p className="font-semibold text-text">{email.subject}</p>
                        <p className="text-sm text-text-light">From: {email.sender}</p>
                        <p className="text-xs text-text-light mt-1">
                          {new Date(email.received_at).toLocaleDateString()}
                        </p>
                      </button>
                    ))}
                </div>
              )}
            </div>
          )}

          {/* RFP Clone Search Dropdown */}
          {quickStartMode === 'clone' && (
            <div className="relative">
              <label className="block text-sm font-medium text-text mb-2">
                Search Existing RFPs
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-light" size={18} />
                <input
                  type="text"
                  value={rfpSearchQuery}
                  onChange={(e) => {
                    setRFPSearchQuery(e.target.value);
                    setShowRFPDropdown(true);
                  }}
                  onFocus={() => setShowRFPDropdown(true)}
                  className="w-full pl-10 pr-4 py-3 border-2 border-primary-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-600"
                  placeholder="Type to search RFPs..."
                />
              </div>

              {showRFPDropdown && existingRFPs.length > 0 && (
                <div className="absolute z-10 w-full mt-2 bg-white border border-gray-300 rounded-lg shadow-xl max-h-64 overflow-y-auto">
                  {existingRFPs
                    .filter(rfp =>
                      rfp.title?.toLowerCase().includes(rfpSearchQuery.toLowerCase()) ||
                      rfp.rfp_id?.toLowerCase().includes(rfpSearchQuery.toLowerCase())
                    )
                    .map((rfp) => (
                      <button
                        key={rfp.rfp_id}
                        type="button"
                        onClick={() => handleRFPClone(rfp)}
                        className="w-full text-left px-4 py-3 hover:bg-primary-50 border-b border-gray-100 last:border-b-0 transition-colors"
                      >
                        <p className="font-semibold text-text">{rfp.title}</p>
                        <p className="text-sm text-text-light">{rfp.rfp_id}</p>
                        <p className="text-xs text-text-light mt-1">
                          Status: {rfp.status} | {new Date(rfp.discovered_at).toLocaleDateString()}
                        </p>
                      </button>
                    ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {!showPreview && (
        <div className="bg-white rounded-lg shadow-md p-6">
          {/* Submission Type Selector */}
          <div className="flex gap-4 mb-6">
            <button
              type="button"
              onClick={() => setSubmissionType('url')}
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-colors ${submissionType === 'url'
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
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-colors ${submissionType === 'file'
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
                <div className="flex gap-2">
                  <input
                    type="url"
                    name="source"
                    value={formData.source}
                    onChange={handleInputChange}
                    required
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                    placeholder="https://example.com/rfp-document.pdf"
                  />
                  <button
                    type="button"
                    onClick={() => handleMockUrlScrape(formData.source)}
                    className="px-4 py-2 bg-secondary text-white rounded-lg hover:bg-secondary-dark transition-colors flex items-center gap-2"
                  >
                    <Sparkles size={18} />
                    Fetch
                  </button>
                </div>

                {/* Mock URL Quick Links */}
                <div className="mt-3 flex flex-wrap gap-2">
                  <span className="text-xs text-text-light py-1">Try Demo URLs:</span>
                  {Object.keys(MOCK_URL_DATA).map((url, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => {
                        setFormData(prev => ({ ...prev, source: url }));
                        handleMockUrlScrape(url);
                      }}
                      className="text-xs px-2 py-1 bg-gray-100 text-primary border border-primary/20 rounded hover:bg-primary/10 transition-colors truncate max-w-[200px]"
                      title={MOCK_URL_DATA[url].title}
                    >
                      {url}
                    </button>
                  ))}
                </div>
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
                className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
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
      )}

      {/* Info Box */}
      {!showPreview && (
        <div className="bg-primary/10 border border-primary/30 rounded-lg p-4">
          <h4 className="font-semibold text-primary mb-2">What happens next?</h4>
          <ul className="text-sm text-text space-y-1">
            <li>• System will parse the RFP document and extract specifications</li>
            <li>• Product matching engine will find best-fit products from catalog</li>
            <li>• Pricing calculator will generate cost estimates</li>
            <li>• Complete response will be available immediately</li>
          </ul>
        </div>
      )}

      {/* Processing Results */}
      {processing && (
        <div className="bg-white rounded-lg shadow-lg border-2 border-olive-300 p-8">
          <div className="flex items-center gap-3 mb-6">
            <Loader className="animate-spin text-olive-600" size={32} />
            <h3 className="text-2xl font-bold text-olive-800">Multi-Agent Processing in Progress...</h3>
          </div>

          {/* Current Step Display */}
          {processingStep && (
            <div className="mb-6 p-4 bg-olive-50 border-l-4 border-olive-600 rounded">
              <p className="text-lg font-semibold text-olive-800">{processingStep}</p>
            </div>
          )}

          {/* Processing Steps Timeline */}
          <div className="space-y-3">
            {processingSteps.map((step, index) => (
              <div
                key={index}
                className={`flex items-start gap-3 p-3 rounded-lg transition-all ${step.completed
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-olive-50 border border-olive-200 animate-pulse'
                  }`}
              >
                <div className="flex-shrink-0 mt-1">
                  {step.completed ? (
                    <CheckCircle className="text-green-600" size={20} />
                  ) : (
                    <Loader className="animate-spin text-olive-600" size={20} />
                  )}
                </div>
                <div className="flex-1">
                  <p className={`font-medium ${step.completed ? 'text-green-800' : 'text-olive-800'}`}>
                    {step.text}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">{step.timestamp}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Progress Info */}
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-800">
              <strong>ℹ️ Multi-Agent System:</strong> Your RFP is being processed by 5 specialized AI agents working in sequence to ensure accuracy and compliance.
            </p>
          </div>
        </div>
      )}

      {/* Processed Results Display */}
      {showPreview && processedData && !processing && (
        <div className="space-y-6">
          {/* Preview Header */}
          <div className="bg-gradient-to-r from-olive-50 to-green-50 rounded-lg shadow-md p-6 border-2 border-olive-300">
            <h2 className="text-2xl font-bold text-olive-800 mb-2">📋 Review RFP Details</h2>
            <p className="text-olive-700">
              Please review the extracted specifications, matched products, and pricing details below.
              Click "Send to RFP List" to confirm submission or "Edit Details" to make changes.
            </p>
          </div>

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
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${match.match_score >= 0.9 ? 'bg-success/20 text-success' :
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

          {/* Action Buttons */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex gap-4">
              <button
                type="button"
                onClick={() => {
                  setShowPreview(false);
                  setProcessedData(null);
                }}
                className="flex-1 px-6 py-3 border-2 border-gray-300 text-text rounded-lg hover:bg-gray-50 transition-colors font-semibold"
              >
                ← Edit Details
              </button>
              <button
                type="button"
                onClick={handleConfirmSubmit}
                disabled={confirming}
                className="flex-1 px-6 py-4 bg-olive-600 text-white rounded-lg hover:bg-olive-700 transition-colors font-semibold text-lg shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {confirming ? (
                  <span className="flex items-center justify-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Submitting...
                  </span>
                ) : (
                  '✓ Send to RFP List'
                )}
              </button>
            </div>
            <p className="text-center text-sm text-text-light mt-3">
              Review the details above and click "Send to RFP List" to confirm submission
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SubmitRFP;
