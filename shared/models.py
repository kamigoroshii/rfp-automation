"""
Data models for RFP Automation System
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional
import json


@dataclass
class RFPSummary:
    """RFP summary from Sales Agent"""
    rfp_id: str
    title: str
    source: str
    deadline: datetime
    scope: str
    testing_requirements: List[str]
    discovered_at: datetime
    status: str  # new, processing, completed, submitted, failed
    go_no_go_score: float = 0.0
    client_tier: str = "Standard"
    project_value: float = 0.0
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        data = asdict(self)
        data['deadline'] = self.deadline.isoformat()
        data['discovered_at'] = self.discovered_at.isoformat()
        return json.dumps(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RFPSummary':
        """Create from dictionary"""
        data['deadline'] = datetime.fromisoformat(data['deadline'])
        data['discovered_at'] = datetime.fromisoformat(data['discovered_at'])
        # Handle optional fields if they don't exist in legacy data
        if 'go_no_go_score' not in data:
            data['go_no_go_score'] = 0.0
        if 'client_tier' not in data:
            data['client_tier'] = "Standard"
        if 'project_value' not in data:
            data['project_value'] = 0.0
        if 'attachments' not in data:
            data['attachments'] = []
        return cls(**data)


@dataclass
class Specification:
    """Technical specifications from Document Agent"""
    rfp_id: str
    specifications: Dict[str, Any]
    testing_requirements: Dict[str, List[str]]
    confidence_score: float
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Specification':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ProductMatch:
    """Product match from Technical Agent"""
    sku: str
    product_name: str
    match_score: float
    specification_alignment: Dict[str, str]
    datasheet_url: str
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductMatch':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class PricingBreakdown:
    """Pricing breakdown from Pricing Agent"""
    sku: str
    unit_price: float
    quantity: int
    subtotal: float
    testing_cost: float
    delivery_cost: float
    urgency_adjustment: float
    total: float
    currency: str = "INR"
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PricingBreakdown':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class RFPResponse:
    """Consolidated RFP response"""
    rfp_id: str
    rfp_summary: RFPSummary
    specifications: Optional[Specification]
    matches: List[ProductMatch]
    pricing: List[PricingBreakdown]
    recommended_sku: Optional[str]
    total_estimate: float
    generated_at: datetime
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        data = {
            'rfp_id': self.rfp_id,
            'rfp_summary': asdict(self.rfp_summary),
            'specifications': asdict(self.specifications) if self.specifications else None,
            'matches': [asdict(m) for m in self.matches],
            'pricing': [asdict(p) for p in self.pricing],
            'recommended_sku': self.recommended_sku,
            'total_estimate': self.total_estimate,
            'generated_at': self.generated_at.isoformat()
        }
        # Convert datetime objects in nested structures
        data['rfp_summary']['deadline'] = self.rfp_summary.deadline.isoformat()
        data['rfp_summary']['discovered_at'] = self.rfp_summary.discovered_at.isoformat()
        return json.dumps(data)


@dataclass
class Feedback:
    """Feedback for Learning Agent"""
    rfp_id: str
    submitted_at: datetime
    outcome: str  # won, lost, pending
    actual_price: Optional[float]
    predicted_price: float
    match_accuracy: Optional[float]
    notes: Optional[str] = None
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        data = asdict(self)
        data['submitted_at'] = self.submitted_at.isoformat()
        return json.dumps(data)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Feedback':
        """Create from dictionary"""
        data['submitted_at'] = datetime.fromisoformat(data['submitted_at'])
        return cls(**data)
