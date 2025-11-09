/**
 * Specification Extractor - Extract technical specs from RFP text
 */

// Voltage patterns
const VOLTAGE_PATTERNS = [
  /(\d+(?:\.\d+)?)\s*k?V/gi,
  /voltage.*?(\d+(?:\.\d+)?)\s*k?V/gi,
  /rated.*?(\d+(?:\.\d+)?)\s*k?V/gi
];

// Current/conductor size patterns
const CONDUCTOR_PATTERNS = [
  /(\d+)\s*(?:sq\.?\s*mm|mm²|sq\s*mm)/gi,
  /conductor.*?(\d+)\s*(?:sq\.?\s*mm|mm²)/gi,
  /size.*?(\d+)\s*(?:sq\.?\s*mm|mm²)/gi
];

// Material patterns
const MATERIAL_PATTERNS = {
  insulation: /(?:XLPE|PVC|EPR|PE)/gi,
  conductor: /(?:copper|aluminum|aluminium|Cu|Al)/gi,
  armor: /(?:SWA|AWA|STA|unarmored|armored)/gi
};

// Standard patterns
const STANDARD_PATTERNS = [
  /IEC\s*\d+(?:-\d+)?/gi,
  /IS\s*\d+/gi,
  /BS\s*\d+/gi,
  /CPRI/gi
];

// Cable type patterns
const CABLE_TYPE_PATTERNS = /(?:HT|LT|MV|LV|HV|control|power|instrumentation)\s*cable/gi;

/**
 * Extract voltage specifications
 */
function extractVoltage(text) {
  const voltages = [];
  
  for (const pattern of VOLTAGE_PATTERNS) {
    const matches = [...text.matchAll(pattern)];
    matches.forEach(match => {
      const value = parseFloat(match[1]);
      if (value && !isNaN(value)) {
        voltages.push({
          type: 'voltage',
          value: value.toString(),
          unit: 'kV',
          confidence: 0.9
        });
      }
    });
  }
  
  // Remove duplicates
  const unique = voltages.reduce((acc, curr) => {
    if (!acc.find(v => v.value === curr.value)) {
      acc.push(curr);
    }
    return acc;
  }, []);
  
  return unique;
}

/**
 * Extract conductor size specifications
 */
function extractConductorSize(text) {
  const sizes = [];
  
  for (const pattern of CONDUCTOR_PATTERNS) {
    const matches = [...text.matchAll(pattern)];
    matches.forEach(match => {
      const value = parseInt(match[1]);
      if (value && !isNaN(value)) {
        sizes.push({
          type: 'conductor_size',
          value: value.toString(),
          unit: 'sq.mm',
          confidence: 0.85
        });
      }
    });
  }
  
  // Remove duplicates
  const unique = sizes.reduce((acc, curr) => {
    if (!acc.find(s => s.value === curr.value)) {
      acc.push(curr);
    }
    return acc;
  }, []);
  
  return unique;
}

/**
 * Extract material specifications
 */
function extractMaterials(text) {
  const materials = [];
  
  // Insulation material
  const insulationMatches = [...text.matchAll(MATERIAL_PATTERNS.insulation)];
  insulationMatches.forEach(match => {
    materials.push({
      type: 'insulation_material',
      value: match[0].toUpperCase(),
      unit: '',
      confidence: 0.9
    });
  });
  
  // Conductor material
  const conductorMatches = [...text.matchAll(MATERIAL_PATTERNS.conductor)];
  conductorMatches.forEach(match => {
    let value = match[0].toLowerCase();
    if (value === 'aluminium') value = 'aluminum';
    if (value === 'cu') value = 'copper';
    if (value === 'al') value = 'aluminum';
    
    materials.push({
      type: 'conductor_material',
      value: value.charAt(0).toUpperCase() + value.slice(1),
      unit: '',
      confidence: 0.85
    });
  });
  
  // Armor type
  const armorMatches = [...text.matchAll(MATERIAL_PATTERNS.armor)];
  armorMatches.forEach(match => {
    materials.push({
      type: 'armor_type',
      value: match[0].toUpperCase(),
      unit: '',
      confidence: 0.8
    });
  });
  
  // Remove duplicates
  const unique = materials.reduce((acc, curr) => {
    if (!acc.find(m => m.type === curr.type && m.value === curr.value)) {
      acc.push(curr);
    }
    return acc;
  }, []);
  
  return unique;
}

/**
 * Extract standards
 */
function extractStandards(text) {
  const standards = [];
  
  for (const pattern of STANDARD_PATTERNS) {
    const matches = [...text.matchAll(pattern)];
    matches.forEach(match => {
      standards.push({
        type: 'standard',
        value: match[0],
        unit: '',
        confidence: 0.95
      });
    });
  }
  
  // Remove duplicates
  const unique = standards.reduce((acc, curr) => {
    if (!acc.find(s => s.value === curr.value)) {
      acc.push(curr);
    }
    return acc;
  }, []);
  
  return unique;
}

/**
 * Extract cable type
 */
function extractCableType(text) {
  const matches = [...text.matchAll(CABLE_TYPE_PATTERNS)];
  
  if (matches.length > 0) {
    return [{
      type: 'cable_type',
      value: matches[0][0],
      unit: '',
      confidence: 0.85
    }];
  }
  
  return [];
}

/**
 * Extract quantity
 */
function extractQuantity(text) {
  const patterns = [
    /(\d+(?:,\d+)?)\s*(?:meters|metre|m|mtr)/gi,
    /quantity.*?(\d+(?:,\d+)?)\s*(?:meters|metre|m)?/gi,
    /supply.*?(\d+(?:,\d+)?)\s*(?:meters|metre|m)/gi
  ];
  
  for (const pattern of patterns) {
    const matches = [...text.matchAll(pattern)];
    if (matches.length > 0) {
      const value = matches[0][1].replace(/,/g, '');
      return [{
        type: 'quantity',
        value: value,
        unit: 'meters',
        confidence: 0.9
      }];
    }
  }
  
  return [];
}

/**
 * Extract number of cores
 */
function extractCores(text) {
  const patterns = [
    /(\d+)\s*core/gi,
    /(\d+)C/gi,
    /(\d+)\s*x\s*\d+/gi  // e.g., "3 x 185"
  ];
  
  for (const pattern of patterns) {
    const matches = [...text.matchAll(pattern)];
    if (matches.length > 0) {
      return [{
        type: 'cores',
        value: matches[0][1],
        unit: 'cores',
        confidence: 0.85
      }];
    }
  }
  
  return [];
}

/**
 * Main extraction function
 */
export function extractSpecifications(text) {
  if (!text || typeof text !== 'string') {
    return [];
  }
  
  const specifications = [
    ...extractVoltage(text),
    ...extractConductorSize(text),
    ...extractMaterials(text),
    ...extractStandards(text),
    ...extractCableType(text),
    ...extractQuantity(text),
    ...extractCores(text)
  ];
  
  return specifications;
}

/**
 * Get specification summary
 */
export function getSpecificationSummary(specifications) {
  const summary = {};
  
  specifications.forEach(spec => {
    if (spec.type === 'voltage') {
      summary.voltage_rating = `${spec.value} ${spec.unit}`;
    } else if (spec.type === 'conductor_size') {
      summary.conductor_size = `${spec.value} ${spec.unit}`;
    } else if (spec.type === 'conductor_material') {
      summary.conductor_material = spec.value;
    } else if (spec.type === 'insulation_material') {
      summary.insulation_type = spec.value;
    } else if (spec.type === 'cable_type') {
      summary.cable_type = spec.value;
    } else if (spec.type === 'quantity') {
      summary.quantity = `${spec.value} ${spec.unit}`;
    } else if (spec.type === 'cores') {
      summary.cores = spec.value;
    } else if (spec.type === 'standard') {
      if (!summary.standards) summary.standards = [];
      summary.standards.push(spec.value);
    }
  });
  
  return summary;
}

/**
 * Validate specifications
 */
export function validateSpecifications(specifications) {
  const validation = {
    isValid: false,
    missingFields: [],
    warnings: []
  };
  
  const hasVoltage = specifications.some(s => s.type === 'voltage');
  const hasConductor = specifications.some(s => s.type === 'conductor_size' || s.type === 'conductor_material');
  const hasInsulation = specifications.some(s => s.type === 'insulation_material');
  
  if (!hasVoltage) {
    validation.missingFields.push('Voltage rating');
  }
  
  if (!hasConductor) {
    validation.missingFields.push('Conductor specification');
  }
  
  if (!hasInsulation) {
    validation.warnings.push('Insulation material not specified');
  }
  
  validation.isValid = hasVoltage && hasConductor;
  
  return validation;
}
