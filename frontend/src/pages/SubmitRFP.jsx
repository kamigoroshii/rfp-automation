import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { rfpAPI } from '../services/api';
import { toast } from 'react-toastify';
import { Upload, Link as LinkIcon, FileText } from 'lucide-react';

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const testingReqs = formData.testing_requirements
        .split(',')
        .map(r => r.trim())
        .filter(r => r);

      const rfpData = {
        title: formData.title,
        source: submissionType === 'url' ? formData.source : `File: ${file?.name || 'uploaded'}`,
        deadline: new Date(formData.deadline).toISOString(),
        scope: formData.scope,
        testing_requirements: testingReqs
      };

      const response = await rfpAPI.submitRFP(rfpData);
      toast.success('RFP submitted successfully! Processing will begin shortly.');
      
      setTimeout(() => {
        navigate(`/rfp/${response.data.rfp_id}`);
      }, 1500);
    } catch (error) {
      console.error('Error submitting RFP:', error);
      toast.error('Failed to submit RFP. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="w-full space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-text">Submit New RFP</h2>
        <p className="text-text-light mt-1">Add a new RFP for automated processing</p>
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
          <li>• Complete response will be available within 30 minutes</li>
        </ul>
      </div>
    </div>
  );
};

export default SubmitRFP;
