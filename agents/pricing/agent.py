"""
Pricing Agent - Calculates pricing for matched products
"""
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

from shared.models import PricingBreakdown, ProductMatch

logger = logging.getLogger(__name__)


class PricingAgent:
    """Agent responsible for calculating pricing estimates"""
    
    def __init__(self):
        self.name = "PricingAgent"
        self.version = "1.0.0"
        
        # Base pricing rules (can be loaded from config/database)
        self.base_prices = {
            'XLPE-11KV-185': 450.00,
            'XLPE-11KV-240': 580.00,
            'XLPE-33KV-185': 850.00,
            'PVC-1.1KV-50': 120.00,
            'XLPE-11KV-300': 520.00
        }
        
        # Testing cost multipliers
        self.testing_costs = {
            'type_test': 0.05,      # 5% of product cost
            'routine_test': 0.02,   # 2% of product cost
            'sample_test': 0.03     # 3% of product cost
        }
        
        logger.info(f"{self.name} v{self.version} initialized")
    
    def calculate_pricing(
        self,
        rfp_id: str,
        matches: List[ProductMatch],
        quantity: int = 1000,  # meters
        deadline: datetime = None,
        testing_requirements: List[str] = None
    ) -> List[PricingBreakdown]:
        """
        Calculate pricing for matched products
        
        Args:
            rfp_id: RFP identifier
            matches: List of ProductMatch objects
            quantity: Required quantity (meters)
            deadline: RFP deadline
            testing_requirements: List of required tests
            
        Returns:
            List of PricingBreakdown objects
        """
        try:
            logger.info(f"Calculating pricing for RFP: {rfp_id}")
            
            pricing_list = []
            
            for match in matches:
                pricing = self._calculate_product_pricing(
                    match,
                    quantity,
                    deadline,
                    testing_requirements or []
                )
                pricing_list.append(pricing)
            
            logger.info(f"Calculated pricing for {len(pricing_list)} products")
            return pricing_list
            
        except Exception as e:
            logger.error(f"Error calculating pricing: {str(e)}")
            return []
    
    def _calculate_product_pricing(
        self,
        match: ProductMatch,
        quantity: int,
        deadline: datetime,
        testing_requirements: List[str]
    ) -> PricingBreakdown:
        """Calculate pricing for a single product"""
        
        # Get base unit price
        unit_price = self.base_prices.get(match.sku, 100.00)
        
        # Apply match score adjustment (lower score = higher price risk)
        if match.match_score < 0.8:
            unit_price *= 1.1  # 10% premium for lower confidence
        
        # Calculate subtotal
        subtotal = unit_price * quantity
        
        # Calculate testing costs
        testing_cost = self._calculate_testing_cost(
            subtotal,
            testing_requirements
        )
        
        # Calculate delivery cost (simplified)
        delivery_cost = self._calculate_delivery_cost(quantity)
        
        # Calculate urgency adjustment
        urgency_adjustment = self._calculate_urgency_adjustment(
            subtotal,
            deadline
        )
        
        # Calculate total
        total = subtotal + testing_cost + delivery_cost + urgency_adjustment
        
        return PricingBreakdown(
            sku=match.sku,
            unit_price=round(unit_price, 2),
            quantity=quantity,
            subtotal=round(subtotal, 2),
            testing_cost=round(testing_cost, 2),
            delivery_cost=round(delivery_cost, 2),
            urgency_adjustment=round(urgency_adjustment, 2),
            total=round(total, 2),
            currency="INR"
        )
    
    def _calculate_testing_cost(
        self,
        subtotal: float,
        testing_requirements: List[str]
    ) -> float:
        """Calculate testing costs based on requirements"""
        testing_cost = 0.0
        
        for test in testing_requirements:
            test_lower = test.lower()
            
            if 'type' in test_lower:
                testing_cost += subtotal * self.testing_costs['type_test']
            elif 'routine' in test_lower:
                testing_cost += subtotal * self.testing_costs['routine_test']
            elif 'sample' in test_lower:
                testing_cost += subtotal * self.testing_costs['sample_test']
        
        return testing_cost
    
    def _calculate_delivery_cost(self, quantity: int) -> float:
        """Calculate delivery/logistics cost"""
        # Base delivery cost
        base_cost = 5000.00
        
        # Additional cost per meter for large orders
        if quantity > 5000:
            base_cost += (quantity - 5000) * 0.5
        
        return base_cost
    
    def _calculate_urgency_adjustment(
        self,
        subtotal: float,
        deadline: datetime
    ) -> float:
        """Calculate urgency adjustment based on deadline"""
        if not deadline:
            return 0.0
        
        days_until_deadline = (deadline - datetime.now()).days
        
        # Apply premium for urgent orders
        if days_until_deadline < 14:
            return subtotal * 0.15  # 15% premium for <2 weeks
        elif days_until_deadline < 30:
            return subtotal * 0.08  # 8% premium for <1 month
        elif days_until_deadline < 60:
            return subtotal * 0.03  # 3% premium for <2 months
        
        return 0.0
    
    def get_recommended_product(
        self,
        pricing_list: List[PricingBreakdown],
        matches: List[ProductMatch]
    ) -> str:
        """
        Get recommended product SKU based on pricing and match score
        
        Args:
            pricing_list: List of PricingBreakdown objects
            matches: List of ProductMatch objects
            
        Returns:
            Recommended SKU
        """
        if not pricing_list or not matches:
            return None
        
        # Create match score dictionary
        match_scores = {m.sku: m.match_score for m in matches}
        
        # Calculate recommendation score (combination of price and match)
        recommendations = []
        
        for pricing in pricing_list:
            match_score = match_scores.get(pricing.sku, 0.0)
            
            # Normalize total price (lower is better, scale 0-1)
            max_total = max(p.total for p in pricing_list)
            price_score = 1.0 - (pricing.total / max_total)
            
            # Combined score (70% match quality, 30% price)
            combined_score = (match_score * 0.7) + (price_score * 0.3)
            
            recommendations.append({
                'sku': pricing.sku,
                'score': combined_score,
                'match_score': match_score,
                'price_score': price_score,
                'total': pricing.total
            })
        
        # Sort by combined score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top recommendation
        if recommendations:
            recommended = recommendations[0]
            logger.info(
                f"Recommended SKU: {recommended['sku']} "
                f"(score: {recommended['score']:.2f}, "
                f"match: {recommended['match_score']:.2f}, "
                f"price: ₹{recommended['total']:,.2f})"
            )
            return recommended['sku']
        
        return None
    
    def apply_discount(
        self,
        pricing: PricingBreakdown,
        discount_percent: float
    ) -> PricingBreakdown:
        """
        Apply discount to pricing
        
        Args:
            pricing: PricingBreakdown object
            discount_percent: Discount percentage (0-100)
            
        Returns:
            Updated PricingBreakdown
        """
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        
        discount_amount = pricing.subtotal * (discount_percent / 100)
        new_total = pricing.total - discount_amount
        
        return PricingBreakdown(
            sku=pricing.sku,
            unit_price=pricing.unit_price,
            quantity=pricing.quantity,
            subtotal=pricing.subtotal - discount_amount,
            testing_cost=pricing.testing_cost,
            delivery_cost=pricing.delivery_cost,
            urgency_adjustment=pricing.urgency_adjustment,
            total=round(new_total, 2),
            currency=pricing.currency
        )
    
    def generate_cost_breakdown_report(
        self,
        pricing: PricingBreakdown
    ) -> Dict[str, Any]:
        """Generate detailed cost breakdown report"""
        
        total = pricing.total
        
        return {
            'sku': pricing.sku,
            'quantity': f"{pricing.quantity} meters",
            'breakdown': {
                'material_cost': {
                    'amount': pricing.subtotal,
                    'percentage': round((pricing.subtotal / total) * 100, 2)
                },
                'testing_cost': {
                    'amount': pricing.testing_cost,
                    'percentage': round((pricing.testing_cost / total) * 100, 2)
                },
                'delivery_cost': {
                    'amount': pricing.delivery_cost,
                    'percentage': round((pricing.delivery_cost / total) * 100, 2)
                },
                'urgency_premium': {
                    'amount': pricing.urgency_adjustment,
                    'percentage': round((pricing.urgency_adjustment / total) * 100, 2)
                }
            },
            'unit_price': pricing.unit_price,
            'total': total,
            'currency': pricing.currency
        }
