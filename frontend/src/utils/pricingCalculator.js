/**
 * Pricing Calculator - Calculate pricing for matched products
 */

// Base pricing configuration
const TESTING_COSTS = {
  type_test: 0.05,      // 5% of product cost
  routine_test: 0.02,   // 2% of product cost
  sample_test: 0.03,    // 3% of product cost
  partial_discharge: 0.02,
  impulse_voltage: 0.03,
  heat_cycle: 0.02
};

const BASE_DELIVERY_COST = 5000.00;
const DELIVERY_COST_PER_METER = 0.5;
const LARGE_ORDER_THRESHOLD = 5000;

/**
 * Calculate testing costs
 */
function calculateTestingCost(subtotal, testingRequirements) {
  let testingCost = 0.0;
  
  if (!testingRequirements || testingRequirements.length === 0) {
    return testingCost;
  }
  
  testingRequirements.forEach(req => {
    const reqLower = req.toLowerCase();
    
    if (reqLower.includes('type')) {
      testingCost += subtotal * TESTING_COSTS.type_test;
    }
    if (reqLower.includes('routine')) {
      testingCost += subtotal * TESTING_COSTS.routine_test;
    }
    if (reqLower.includes('sample')) {
      testingCost += subtotal * TESTING_COSTS.sample_test;
    }
    if (reqLower.includes('partial discharge')) {
      testingCost += subtotal * TESTING_COSTS.partial_discharge;
    }
    if (reqLower.includes('impulse')) {
      testingCost += subtotal * TESTING_COSTS.impulse_voltage;
    }
    if (reqLower.includes('heat cycle')) {
      testingCost += subtotal * TESTING_COSTS.heat_cycle;
    }
  });
  
  return testingCost;
}

/**
 * Calculate delivery cost
 */
function calculateDeliveryCost(quantity) {
  let deliveryCost = BASE_DELIVERY_COST;
  
  if (quantity > LARGE_ORDER_THRESHOLD) {
    deliveryCost += (quantity - LARGE_ORDER_THRESHOLD) * DELIVERY_COST_PER_METER;
  }
  
  return deliveryCost;
}

/**
 * Calculate urgency adjustment
 */
function calculateUrgencyAdjustment(subtotal, deadline) {
  if (!deadline) {
    return 0.0;
  }
  
  const deadlineDate = new Date(deadline);
  const now = new Date();
  const daysUntilDeadline = Math.floor((deadlineDate - now) / (1000 * 60 * 60 * 24));
  
  if (daysUntilDeadline < 14) {
    return subtotal * 0.15;  // 15% premium for <2 weeks
  } else if (daysUntilDeadline < 30) {
    return subtotal * 0.08;  // 8% premium for <1 month
  } else if (daysUntilDeadline < 60) {
    return subtotal * 0.03;  // 3% premium for <2 months
  }
  
  return 0.0;
}

/**
 * Calculate pricing for a single product
 */
function calculateProductPricing(match, quantity, deadline, testingRequirements) {
  // Get base unit price
  let unitPrice = match.unit_price || 100.00;
  
  // Apply match score adjustment (lower score = higher price risk)
  if (match.match_score < 0.8) {
    unitPrice *= 1.1;  // 10% premium for lower confidence
  }
  
  // Calculate subtotal
  const subtotal = unitPrice * quantity;
  
  // Calculate testing costs
  const testingCost = calculateTestingCost(subtotal, testingRequirements);
  
  // Calculate delivery cost
  const deliveryCost = calculateDeliveryCost(quantity);
  
  // Calculate urgency adjustment
  const urgencyAdjustment = calculateUrgencyAdjustment(subtotal, deadline);
  
  // Calculate total
  const total = subtotal + testingCost + deliveryCost + urgencyAdjustment;
  
  return {
    sku: match.sku,
    product_name: match.name,
    unit_price: parseFloat(unitPrice.toFixed(2)),
    quantity,
    subtotal: parseFloat(subtotal.toFixed(2)),
    testing_cost: parseFloat(testingCost.toFixed(2)),
    delivery_cost: parseFloat(deliveryCost.toFixed(2)),
    urgency_adjustment: parseFloat(urgencyAdjustment.toFixed(2)),
    total: parseFloat(total.toFixed(2)),
    currency: 'INR'
  };
}

/**
 * Calculate pricing for all matched products
 */
export function calculatePricing(matches, quantity, deadline, testingRequirements) {
  if (!matches || matches.length === 0) {
    return [];
  }
  
  return matches.map(match => 
    calculateProductPricing(match, quantity, deadline, testingRequirements)
  );
}

/**
 * Generate cost breakdown report
 */
export function generateCostBreakdown(pricing) {
  const total = pricing.total;
  
  return {
    sku: pricing.sku,
    product_name: pricing.product_name,
    quantity: `${pricing.quantity} meters`,
    breakdown: {
      material_cost: {
        amount: pricing.subtotal,
        percentage: parseFloat(((pricing.subtotal / total) * 100).toFixed(2))
      },
      testing_cost: {
        amount: pricing.testing_cost,
        percentage: parseFloat(((pricing.testing_cost / total) * 100).toFixed(2))
      },
      delivery_cost: {
        amount: pricing.delivery_cost,
        percentage: parseFloat(((pricing.delivery_cost / total) * 100).toFixed(2))
      },
      urgency_premium: {
        amount: pricing.urgency_adjustment,
        percentage: parseFloat(((pricing.urgency_adjustment / total) * 100).toFixed(2))
      }
    },
    unit_price: pricing.unit_price,
    total: total,
    currency: pricing.currency
  };
}

/**
 * Apply discount to pricing
 */
export function applyDiscount(pricing, discountPercent) {
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Discount must be between 0 and 100');
  }
  
  const discountAmount = pricing.subtotal * (discountPercent / 100);
  const newTotal = pricing.total - discountAmount;
  
  return {
    ...pricing,
    discount_percent: discountPercent,
    discount_amount: parseFloat(discountAmount.toFixed(2)),
    subtotal: parseFloat((pricing.subtotal - discountAmount).toFixed(2)),
    total: parseFloat(newTotal.toFixed(2))
  };
}

/**
 * Format currency
 */
export function formatCurrency(amount, currency = 'INR') {
  if (currency === 'INR') {
    // Format in lakhs for large amounts
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(2)}L`;
    }
    return `₹${amount.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`;
  }
  
  return `${currency} ${amount.toLocaleString()}`;
}

/**
 * Get pricing summary
 */
export function getPricingSummary(pricingList) {
  if (!pricingList || pricingList.length === 0) {
    return null;
  }
  
  const lowest = pricingList.reduce((min, p) => p.total < min.total ? p : min);
  const highest = pricingList.reduce((max, p) => p.total > max.total ? p : max);
  const average = pricingList.reduce((sum, p) => sum + p.total, 0) / pricingList.length;
  
  return {
    lowest: {
      sku: lowest.sku,
      total: lowest.total,
      formatted: formatCurrency(lowest.total)
    },
    highest: {
      sku: highest.sku,
      total: highest.total,
      formatted: formatCurrency(highest.total)
    },
    average: {
      total: parseFloat(average.toFixed(2)),
      formatted: formatCurrency(average)
    },
    options_count: pricingList.length
  };
}
