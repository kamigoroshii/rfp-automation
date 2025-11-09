/**
 * Product Matcher - Match specifications with products
 */

// Product catalog (same as backend)
const PRODUCT_CATALOG = [
  {
    sku: 'XLPE-11KV-185',
    name: '11kV XLPE Cable 3x185 sq.mm Aluminum',
    category: 'MV Power Cable',
    specifications: {
      voltage: '11',
      voltage_unit: 'kV',
      conductor_size: '185',
      conductor_material: 'Aluminum',
      insulation_material: 'XLPE',
      cores: '3',
      armor_type: 'SWA'
    },
    standards: ['IEC 60502-2', 'IS 7098'],
    unit_price: 450.00
  },
  {
    sku: 'XLPE-11KV-240',
    name: '11kV XLPE Cable 3x240 sq.mm Aluminum',
    category: 'MV Power Cable',
    specifications: {
      voltage: '11',
      voltage_unit: 'kV',
      conductor_size: '240',
      conductor_material: 'Aluminum',
      insulation_material: 'XLPE',
      cores: '3',
      armor_type: 'SWA'
    },
    standards: ['IEC 60502-2', 'IS 7098'],
    unit_price: 580.00
  },
  {
    sku: 'XLPE-33KV-185',
    name: '33kV XLPE Cable 3x185 sq.mm Copper',
    category: 'HV Power Cable',
    specifications: {
      voltage: '33',
      voltage_unit: 'kV',
      conductor_size: '185',
      conductor_material: 'Copper',
      insulation_material: 'XLPE',
      cores: '3',
      armor_type: 'SWA'
    },
    standards: ['IEC 60502-2', 'IS 7098'],
    unit_price: 850.00
  },
  {
    sku: 'PVC-1.1KV-50',
    name: '1.1kV PVC Cable 4x50 sq.mm Copper',
    category: 'LV Power Cable',
    specifications: {
      voltage: '1.1',
      voltage_unit: 'kV',
      conductor_size: '50',
      conductor_material: 'Copper',
      insulation_material: 'PVC',
      cores: '4',
      armor_type: 'Unarmored'
    },
    standards: ['IS 1554', 'IEC 60227'],
    unit_price: 120.00
  },
  {
    sku: 'XLPE-11KV-300',
    name: '11kV XLPE Cable 3x300 sq.mm Aluminum',
    category: 'MV Power Cable',
    specifications: {
      voltage: '11',
      voltage_unit: 'kV',
      conductor_size: '300',
      conductor_material: 'Aluminum',
      insulation_material: 'XLPE',
      cores: '3',
      armor_type: 'SWA'
    },
    standards: ['IEC 60502-2', 'IS 7098'],
    unit_price: 650.00
  },
  {
    sku: 'XLPE-22KV-240',
    name: '22kV XLPE Cable 3x240 sq.mm Aluminum',
    category: 'MV Power Cable',
    specifications: {
      voltage: '22',
      voltage_unit: 'kV',
      conductor_size: '240',
      conductor_material: 'Aluminum',
      insulation_material: 'XLPE',
      cores: '3',
      armor_type: 'SWA'
    },
    standards: ['IEC 60502-2', 'IS 7098'],
    unit_price: 780.00
  }
];

/**
 * Calculate match score between RFP specs and product
 */
function calculateMatchScore(rfpSpecs, product) {
  let score = 0;
  let maxScore = 0;
  const matchedSpecs = [];
  
  // Extract RFP specification values
  const rfpVoltage = rfpSpecs.find(s => s.type === 'voltage');
  const rfpConductorSize = rfpSpecs.find(s => s.type === 'conductor_size');
  const rfpConductorMaterial = rfpSpecs.find(s => s.type === 'conductor_material');
  const rfpInsulationMaterial = rfpSpecs.find(s => s.type === 'insulation_material');
  const rfpStandards = rfpSpecs.filter(s => s.type === 'standard').map(s => s.value);
  const rfpCores = rfpSpecs.find(s => s.type === 'cores');
  
  // Voltage matching (weight: 30)
  if (rfpVoltage) {
    maxScore += 30;
    if (product.specifications.voltage === rfpVoltage.value) {
      score += 30;
      matchedSpecs.push('voltage');
    } else {
      // Partial match for close voltage ratings
      const voltageDiff = Math.abs(parseFloat(product.specifications.voltage) - parseFloat(rfpVoltage.value));
      if (voltageDiff <= 5) {
        score += 15;
      }
    }
  }
  
  // Conductor size matching (weight: 25)
  if (rfpConductorSize) {
    maxScore += 25;
    if (product.specifications.conductor_size === rfpConductorSize.value) {
      score += 25;
      matchedSpecs.push('conductor_size');
    } else {
      // Partial match for similar conductor sizes
      const sizeDiff = Math.abs(parseInt(product.specifications.conductor_size) - parseInt(rfpConductorSize.value));
      if (sizeDiff <= 50) {
        score += 15;
      } else if (sizeDiff <= 100) {
        score += 10;
      }
    }
  }
  
  // Conductor material matching (weight: 20)
  if (rfpConductorMaterial) {
    maxScore += 20;
    if (product.specifications.conductor_material.toLowerCase() === rfpConductorMaterial.value.toLowerCase()) {
      score += 20;
      matchedSpecs.push('conductor_material');
    }
  }
  
  // Insulation material matching (weight: 15)
  if (rfpInsulationMaterial) {
    maxScore += 15;
    if (product.specifications.insulation_material.toLowerCase() === rfpInsulationMaterial.value.toLowerCase()) {
      score += 15;
      matchedSpecs.push('insulation_material');
    }
  }
  
  // Cores matching (weight: 5)
  if (rfpCores) {
    maxScore += 5;
    if (product.specifications.cores === rfpCores.value) {
      score += 5;
      matchedSpecs.push('cores');
    }
  }
  
  // Standards matching (weight: 5)
  if (rfpStandards.length > 0) {
    maxScore += 5;
    const commonStandards = rfpStandards.filter(std => 
      product.standards.some(pStd => pStd.toLowerCase().includes(std.toLowerCase()))
    );
    if (commonStandards.length > 0) {
      score += 5 * (commonStandards.length / rfpStandards.length);
      matchedSpecs.push('standards');
    }
  }
  
  // Calculate final score (0-1 scale)
  const finalScore = maxScore > 0 ? score / maxScore : 0;
  
  return {
    score: parseFloat(finalScore.toFixed(2)),
    matchedSpecs
  };
}

/**
 * Match products to RFP specifications
 */
export function matchProducts(specifications) {
  if (!specifications || specifications.length === 0) {
    return [];
  }
  
  const matches = PRODUCT_CATALOG.map(product => {
    const { score, matchedSpecs } = calculateMatchScore(specifications, product);
    
    return {
      sku: product.sku,
      name: product.name,
      category: product.category,
      match_score: score,
      matched_specs: matchedSpecs,
      specifications: product.specifications,
      standards: product.standards,
      unit_price: product.unit_price
    };
  });
  
  // Filter out very low matches and sort by score
  return matches
    .filter(m => m.match_score >= 0.3)
    .sort((a, b) => b.match_score - a.match_score);
}

/**
 * Get recommended product
 */
export function getRecommendedProduct(matches, pricingList) {
  if (!matches || matches.length === 0) {
    return null;
  }
  
  // If no pricing, recommend highest match
  if (!pricingList || pricingList.length === 0) {
    return matches[0].sku;
  }
  
  // Calculate combined score (70% match, 30% price)
  const recommendations = matches.map(match => {
    const pricing = pricingList.find(p => p.sku === match.sku);
    if (!pricing) return null;
    
    // Normalize price score (lower is better)
    const maxTotal = Math.max(...pricingList.map(p => p.total));
    const priceScore = 1.0 - (pricing.total / maxTotal);
    
    const combinedScore = (match.match_score * 0.7) + (priceScore * 0.3);
    
    return {
      sku: match.sku,
      combinedScore,
      matchScore: match.match_score,
      priceScore,
      total: pricing.total
    };
  }).filter(r => r !== null);
  
  // Sort by combined score
  recommendations.sort((a, b) => b.combinedScore - a.combinedScore);
  
  return recommendations.length > 0 ? recommendations[0].sku : null;
}

/**
 * Get product catalog
 */
export function getProductCatalog() {
  return PRODUCT_CATALOG;
}

/**
 * Search products by keyword
 */
export function searchProducts(query) {
  if (!query || query.trim() === '') {
    return PRODUCT_CATALOG;
  }
  
  const queryLower = query.toLowerCase();
  
  return PRODUCT_CATALOG.filter(product => 
    product.name.toLowerCase().includes(queryLower) ||
    product.sku.toLowerCase().includes(queryLower) ||
    product.category.toLowerCase().includes(queryLower) ||
    Object.values(product.specifications).some(v => 
      v.toString().toLowerCase().includes(queryLower)
    )
  );
}
