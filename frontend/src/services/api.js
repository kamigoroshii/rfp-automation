import axios from 'axios';
import { mockRFPs, mockRFPDetails, mockAnalytics, mockProducts } from './mockData';

// Set to true to use mock data, false to use real API
const USE_MOCK_DATA = false;

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Simulate network delay
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// RFP API Services
export const rfpAPI = {
  // Get list of all RFPs
  async getRFPs(params = {}) {
    if (USE_MOCK_DATA) {
      await delay(300);
      let filteredRFPs = [...mockRFPs];

      // Apply filters if provided
      if (params.status) {
        filteredRFPs = filteredRFPs.filter(rfp => rfp.status === params.status);
      }

      return { data: { rfps: filteredRFPs, total: filteredRFPs.length } };
    }
    return api.get('/rfp/list', { params });
  },

  // Get specific RFP details
  async getRFP(rfpId) {
    if (USE_MOCK_DATA) {
      await delay(300);
      const details = mockRFPDetails[rfpId];
      if (!details) {
        // Generate basic details from list
        const rfp = mockRFPs.find(r => r.rfp_id === rfpId);
        if (rfp) {
          return {
            data: {
              rfp_summary: rfp,
              specifications: {},
              matches: [],
              pricing: [],
              confidence: 0
            }
          };
        }
        throw new Error('RFP not found');
      }
      return { data: details };
    }
    return api.get(`/rfp/${rfpId}`);
  },

  // Submit new RFP
  async submitRFP(rfpData) {
    if (USE_MOCK_DATA) {
      await delay(500);
      const newRFPId = `RFP-2025-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`;
      const newRFP = {
        rfp_id: newRFPId,
        title: rfpData.title,
        source: rfpData.source,
        deadline: rfpData.deadline,
        scope: rfpData.scope,
        testing_requirements: rfpData.testing_requirements || [],
        discovered_at: new Date().toISOString(),
        status: rfpData.status || 'processing',
        match_score: rfpData.match_score || 0,
        total_estimate: rfpData.total_estimate || 0
      };

      // Add to mock RFPs list
      mockRFPs.unshift(newRFP);

      // Create detailed entry if processing results are included
      if (rfpData.specifications && rfpData.matched_products) {
        mockRFPDetails[newRFPId] = {
          rfp_summary: newRFP,
          specifications: rfpData.specifications,
          testing_requirements: {
            routine_tests: rfpData.testing_requirements,
            certifications: []
          },
          matches: [], // Will be populated by frontend
          pricing: [], // Will be populated by frontend
          recommended_sku: rfpData.recommended_sku || null,
          total_estimate: rfpData.total_estimate || 0,
          generated_at: new Date().toISOString(),
          confidence: rfpData.match_score || 0
        };
      }

      return { data: newRFP };
    }

    // If no file, use JSON endpoint with detailed results
    if (!rfpData.file) {
      return api.post('/rfp/create-json', rfpData);
    }

    // Create FormData for backend API (expects multipart/form-data)
    const formData = new FormData();
    formData.append('title', rfpData.title);
    formData.append('source', rfpData.source);
    formData.append('deadline', rfpData.deadline);
    formData.append('scope', rfpData.scope);

    // Convert testing_requirements array to comma-separated string
    const testingReqs = Array.isArray(rfpData.testing_requirements)
      ? rfpData.testing_requirements.join(', ')
      : rfpData.testing_requirements || '';
    formData.append('testing_requirements', testingReqs);

    // Add file if present
    formData.append('file', rfpData.file);

    return api.post('/rfp/submit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Submit feedback for RFP
  async submitFeedback(rfpId, feedback) {
    if (USE_MOCK_DATA) {
      await delay(300);
      return { data: { success: true, message: 'Feedback recorded' } };
    }
    return api.post(`/rfp/${rfpId}/feedback`, feedback);
  },

  // Generate Proposal PDF
  async generateProposalPDF(rfpId) {
    return api.post(`/rfp/${rfpId}/generate-pdf`);
  },

  // Generate Proposal Word Doc
  async generateProposalDoc(rfpId) {
    return api.post(`/rfp/${rfpId}/generate-doc`);
  }
};

// Analytics API Services
export const analyticsAPI = {
  // Get dashboard analytics
  async getDashboardData() {
    if (USE_MOCK_DATA) {
      await delay(300);
      return { data: mockAnalytics };
    }
    return api.get('/analytics/dashboard');
  }
};



// Product API Services
export const productAPI = {
  // Get products list
  async getProducts(params = {}) {
    if (USE_MOCK_DATA) {
      await delay(300);
      return { data: { products: mockProducts, total: mockProducts.length } };
    }
    return api.get('/products/list', { params });
  },

  // Search products
  async searchProducts(query = '') {
    if (USE_MOCK_DATA) {
      await delay(300);
      const filtered = mockProducts.filter(p =>
        p.product_name.toLowerCase().includes(query.toLowerCase()) ||
        p.sku.toLowerCase().includes(query.toLowerCase())
      );
      return { data: { products: filtered, total: filtered.length } };
    }
    return api.get('/products/search', { params: { query } });
  }
};

// Email API Services
export const emailAPI = {
  // Get list of emails
  async getEmails(status = null) {
    const params = status ? { status } : {};
    return api.get('/emails/list', { params });
  },

  // Get email stats
  async getEmailStats() {
    return api.get('/emails/stats');
  },

  // Get specific email
  async getEmail(emailId) {
    return api.get(`/emails/${emailId}`);
  }
};

// Auditor API Services
export const auditorAPI = {
  // Get audit reports
  async getReports(limit = 50, offset = 0) {
    return api.get('/auditor/reports', { params: { limit, offset } });
  },

  // Validate RFP
  async validateRFP(rfpData) {
    return api.post('/auditor/validate/rfp', rfpData);
  },

  // Generate full audit report
  async generateReport(auditRequest) {
    return api.post('/auditor/audit/complete', auditRequest);
  }
};

export default api;
