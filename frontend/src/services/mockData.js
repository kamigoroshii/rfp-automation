// Mock data for RFP Automation System
// This provides realistic sample data for the frontend to work fully without backend

export const mockRFPs = [
  {
    rfp_id: 'RFP-2025-001',
    title: 'Supply of 11kV XLPE Cables for Metro Project',
    source: 'https://tenders.gov.in/rfp-001',
    deadline: '2025-12-15T17:00:00Z',
    scope: 'Supply of 5000m 11kV XLPE cables with aluminum conductor',
    testing_requirements: ['IEC 60502', 'Type test', 'Routine test'],
    discovered_at: '2025-11-01T10:30:00Z',
    status: 'completed',
    match_score: 0.94,
    total_estimate: 4450000.00
  },
  {
    rfp_id: 'RFP-2025-002',
    title: 'HT Cable Supply for Industrial Plant',
    source: 'Email: procurement@company.com',
    deadline: '2025-11-25T17:00:00Z',
    scope: 'Supply of 3000m 33kV XLPE cables with copper conductor',
    testing_requirements: ['IEC 60502-2', 'IS 7098', 'CPRI certification'],
    discovered_at: '2025-11-05T14:20:00Z',
    status: 'processing',
    match_score: 0.89,
    total_estimate: 5200000.00
  },
  {
    rfp_id: 'RFP-2025-003',
    title: 'LT Power Cable for Commercial Building',
    source: 'https://construction-tenders.com/rfp-003',
    deadline: '2025-11-18T17:00:00Z',
    scope: 'Supply of 8000m 1.1kV PVC cables, 4 core, copper conductor',
    testing_requirements: ['IS 1554', 'Routine tests'],
    discovered_at: '2025-11-08T09:15:00Z',
    status: 'new',
    match_score: 0.92,
    total_estimate: 1850000.00
  },
  {
    rfp_id: 'RFP-2025-004',
    title: 'Control Cables for Automation System',
    source: 'https://industrial-supply.com/rfp-004',
    deadline: '2025-12-01T17:00:00Z',
    scope: 'Supply of 2000m control cables, 12 core, 1.5 sq.mm',
    testing_requirements: ['IEC 60227', 'Fire resistance test'],
    discovered_at: '2025-11-03T11:45:00Z',
    status: 'completed',
    match_score: 0.87,
    total_estimate: 380000.00
  },
  {
    rfp_id: 'RFP-2025-005',
    title: 'MV Cable Supply for Power Distribution',
    source: 'Email: tender@electricity.gov',
    deadline: '2025-12-20T17:00:00Z',
    scope: 'Supply of 4500m 22kV XLPE cables with aluminum conductor',
    testing_requirements: ['IEC 60502-2', 'Type test', 'Partial discharge test'],
    discovered_at: '2025-11-06T16:30:00Z',
    status: 'processing',
    match_score: 0.91,
    total_estimate: 6750000.00
  },
  {
    rfp_id: 'RFP-2025-006',
    title: 'Fiber Optic Cable for Telecom Network',
    source: 'https://telecom-tenders.net/rfp-006',
    deadline: '2025-11-28T17:00:00Z',
    scope: 'Supply of 10000m single mode fiber optic cable, 24 core',
    testing_requirements: ['IEC 60794', 'Attenuation test'],
    discovered_at: '2025-11-07T13:20:00Z',
    status: 'new',
    match_score: 0.85,
    total_estimate: 1200000.00
  }
];

export const mockRFPDetails = {
  'RFP-2025-001': {
    rfp_summary: mockRFPs[0],
    specifications: {
      cable_type: 'XLPE',
      voltage_rating: '11kV',
      conductor_material: 'Aluminum',
      conductor_size: '240 sq.mm',
      insulation_type: 'XLPE',
      quantity: '5000m',
      standards: ['IEC 60502-2', 'IS 7098']
    },
    testing_requirements: {
      type_tests: ['Partial discharge', 'Impulse voltage', 'Heat cycle test'],
      routine_tests: ['Conductor resistance', 'Voltage test', 'Hot set test'],
      certifications: ['BIS', 'CPRI']
    },
    matches: [
      {
        sku: 'XLPE-11KV-AL-240',
        product_name: '11kV XLPE Aluminum Cable 240 sq.mm',
        match_score: 0.94,
        specification_alignment: {
          voltage_rating: 'exact_match',
          conductor_material: 'exact_match',
          conductor_size: 'exact_match',
          insulation_type: 'exact_match'
        },
        datasheet_url: 'https://oem.com/products/XLPE-11KV-AL-240.pdf'
      },
      {
        sku: 'XLPE-11KV-AL-300',
        product_name: '11kV XLPE Aluminum Cable 300 sq.mm',
        match_score: 0.87,
        specification_alignment: {
          voltage_rating: 'exact_match',
          conductor_material: 'exact_match',
          conductor_size: 'close_match',
          insulation_type: 'exact_match'
        },
        datasheet_url: 'https://oem.com/products/XLPE-11KV-AL-300.pdf'
      },
      {
        sku: 'XLPE-11KV-AL-185',
        product_name: '11kV XLPE Aluminum Cable 185 sq.mm',
        match_score: 0.82,
        specification_alignment: {
          voltage_rating: 'exact_match',
          conductor_material: 'exact_match',
          conductor_size: 'close_match',
          insulation_type: 'exact_match'
        },
        datasheet_url: 'https://oem.com/products/XLPE-11KV-AL-185.pdf'
      }
    ],
    pricing: [
      {
        sku: 'XLPE-11KV-AL-240',
        unit_price: 850.00,
        quantity: 5000,
        subtotal: 4250000.00,
        testing_cost: 125000.00,
        delivery_cost: 75000.00,
        urgency_adjustment: 0.00,
        total: 4450000.00,
        currency: 'INR'
      },
      {
        sku: 'XLPE-11KV-AL-300',
        unit_price: 1050.00,
        quantity: 5000,
        subtotal: 5250000.00,
        testing_cost: 125000.00,
        delivery_cost: 75000.00,
        urgency_adjustment: 0.00,
        total: 5450000.00,
        currency: 'INR'
      },
      {
        sku: 'XLPE-11KV-AL-185',
        unit_price: 680.00,
        quantity: 5000,
        subtotal: 3400000.00,
        testing_cost: 125000.00,
        delivery_cost: 75000.00,
        urgency_adjustment: 0.00,
        total: 3600000.00,
        currency: 'INR'
      }
    ],
    recommended_sku: 'XLPE-11KV-AL-240',
    total_estimate: 4450000.00,
    generated_at: '2025-11-01T11:45:00Z',
    confidence: 0.92
  }
};

export const mockAnalytics = {
  overview: {
    total_rfps: 45,
    completed: 32,
    in_progress: 8,
    new: 5,
    win_rate: 0.68,
    avg_processing_time: 18.5,
    avg_match_accuracy: 0.91
  },
  trends: {
    win_rate_trend: [
      { month: 'Jun', rate: 0.62 },
      { month: 'Jul', rate: 0.65 },
      { month: 'Aug', rate: 0.67 },
      { month: 'Sep', rate: 0.64 },
      { month: 'Oct', rate: 0.70 },
      { month: 'Nov', rate: 0.68 }
    ],
    processing_time_trend: [
      { month: 'Jun', time: 22.3 },
      { month: 'Jul', time: 20.1 },
      { month: 'Aug', time: 19.5 },
      { month: 'Sep', time: 18.8 },
      { month: 'Oct', time: 17.9 },
      { month: 'Nov', time: 18.5 }
    ],
    match_accuracy_trend: [
      { month: 'Jun', accuracy: 0.87 },
      { month: 'Jul', accuracy: 0.88 },
      { month: 'Aug', accuracy: 0.89 },
      { month: 'Sep', accuracy: 0.90 },
      { month: 'Oct', accuracy: 0.92 },
      { month: 'Nov', accuracy: 0.91 }
    ]
  },
  revenue: {
    total_value: 125000000,
    won_value: 85000000,
    pipeline_value: 40000000
  }
};

export const mockProducts = [
  {
    sku: 'XLPE-11KV-AL-240',
    product_name: '11kV XLPE Aluminum Cable 240 sq.mm',
    category: 'MV Power Cable',
    specifications: {
      voltage_rating: '11kV',
      conductor_material: 'Aluminum',
      conductor_size: '240 sq.mm',
      insulation_type: 'XLPE',
      armor_type: 'SWA'
    },
    unit_price: 850.00,
    stock_status: 'In Stock',
    datasheet_url: 'https://oem.com/products/XLPE-11KV-AL-240.pdf'
  },
  {
    sku: 'XLPE-33KV-CU-300',
    product_name: '33kV XLPE Copper Cable 300 sq.mm',
    category: 'HV Power Cable',
    specifications: {
      voltage_rating: '33kV',
      conductor_material: 'Copper',
      conductor_size: '300 sq.mm',
      insulation_type: 'XLPE',
      armor_type: 'SWA'
    },
    unit_price: 1850.00,
    stock_status: 'In Stock',
    datasheet_url: 'https://oem.com/products/XLPE-33KV-CU-300.pdf'
  },
  {
    sku: 'PVC-1.1KV-CU-4C',
    product_name: '1.1kV PVC Cable 4 Core Copper',
    category: 'LV Power Cable',
    specifications: {
      voltage_rating: '1.1kV',
      conductor_material: 'Copper',
      cores: '4',
      conductor_size: '16 sq.mm',
      insulation_type: 'PVC'
    },
    unit_price: 245.00,
    stock_status: 'In Stock',
    datasheet_url: 'https://oem.com/products/PVC-1.1KV-CU-4C.pdf'
  }
];
