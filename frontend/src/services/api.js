import axios from 'axios';
import { mockRFPs, mockRFPDetails, mockAnalytics, mockProducts } from './mockData';

// Set to true to use mock data, false to use real API
const USE_MOCK_DATA = true;

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
      const newRFP = {
        rfp_id: `RFP-2025-${String(Math.floor(Math.random() * 1000)).padStart(3, '0')}`,
        ...rfpData,
        discovered_at: new Date().toISOString(),
        status: 'processing',
        match_score: 0,
        total_estimate: 0
      };
      mockRFPs.unshift(newRFP);
      return { data: newRFP };
    }
    return api.post('/rfp/submit', rfpData);
  },

  // Submit feedback for RFP
  async submitFeedback(rfpId, feedback) {
    if (USE_MOCK_DATA) {
      await delay(300);
      return { data: { success: true, message: 'Feedback recorded' } };
    }
    return api.post(`/rfp/${rfpId}/feedback`, feedback);
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

export default api;
