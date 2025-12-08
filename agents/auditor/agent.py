"""
Auditor Agent - Red Team validation and compliance checking
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from shared.models import RFPSummary, ProductMatch, PricingBreakdown

logger = logging.getLogger(__name__)


class AuditorAgent:
    """Agent responsible for validation, compliance, and quality assurance"""
    
    def __init__(self):
        self.name = "AuditorAgent"
        self.version = "1.0.0"
        
        # Compliance rules
        self.compliance_rules = {
            "min_deadline_days": 3,  # Minimum days to deadline
            "max_price_deviation": 0.25,  # 25% max deviation from historical
            "required_specs": ["voltage", "conductor_size", "conductor_material"],
            "required_testing": ["Type Test", "Routine Test"],
            "min_match_score": 0.70,  # Minimum acceptable match score
        }
        
        logger.info(f"{self.name} v{self.version} initialized")
    
    def validate_rfp(self, rfp: RFPSummary) -> Dict[str, Any]:
        """
        Comprehensive RFP validation
        
        Args:
            rfp: RFPSummary object to validate
            
        Returns:
            Validation report with issues and compliance status
        """
        logger.info(f"Validating RFP: {rfp.rfp_id}")
        
        issues = []
        warnings = []
        compliance_checks = {}
        
        # 1. Completeness Check
        completeness = self._check_completeness(rfp)
        compliance_checks["completeness"] = completeness
        if not completeness["passed"]:
            issues.extend(completeness["issues"])
        
        # 2. Deadline Validation
        deadline_check = self._check_deadline(rfp)
        compliance_checks["deadline"] = deadline_check
        if not deadline_check["passed"]:
            if deadline_check["severity"] == "critical":
                issues.append(deadline_check["message"])
            else:
                warnings.append(deadline_check["message"])
        
        # 3. Specification Validation
        spec_check = self._check_specifications(rfp)
        compliance_checks["specifications"] = spec_check
        if not spec_check["passed"]:
            issues.extend(spec_check["issues"])
        
        # 4. Testing Requirements
        testing_check = self._check_testing_requirements(rfp)
        compliance_checks["testing"] = testing_check
        if not testing_check["passed"]:
            warnings.extend(testing_check["warnings"])
        
        # Overall compliance status
        is_compliant = len(issues) == 0
        compliance_score = self._calculate_compliance_score(compliance_checks)
        
        report = {
            "rfp_id": rfp.rfp_id,
            "is_compliant": is_compliant,
            "compliance_score": compliance_score,
            "issues": issues,
            "warnings": warnings,
            "checks": compliance_checks,
            "recommendation": "APPROVE" if is_compliant else "REJECT" if len(issues) > 3 else "REVIEW",
            "validated_at": datetime.now().isoformat()
        }
        
        logger.info(f"Validation complete: {report['recommendation']} (Score: {compliance_score:.2f})")
        return report
    
    def validate_matches(
        self,
        rfp: RFPSummary,
        matches: List[ProductMatch]
    ) -> Dict[str, Any]:
        """
        Validate product matches for quality and appropriateness
        
        Args:
            rfp: RFP being matched
            matches: List of product matches
            
        Returns:
            Match validation report
        """
        logger.info(f"Validating {len(matches)} product matches for RFP {rfp.rfp_id}")
        
        issues = []
        warnings = []
        
        # 1. Check if we have matches
        if not matches:
            issues.append("No product matches found")
            return {
                "passed": False,
                "issues": issues,
                "warnings": warnings,
                "best_match_score": 0
            }
        
        # 2. Check match quality
        best_score = max(m.match_score for m in matches)
        avg_score = sum(m.match_score for m in matches) / len(matches)
        
        if best_score < self.compliance_rules["min_match_score"]:
            issues.append(
                f"Best match score ({best_score:.2f}) below minimum threshold "
                f"({self.compliance_rules['min_match_score']})"
            )
        
        if avg_score < 0.60:
            warnings.append(f"Average match score is low ({avg_score:.2f})")
        
        # 3. Check for specification alignment
        for match in matches[:3]:  # Top 3 matches
            if not match.specification_alignment:
                warnings.append(f"Match {match.sku} missing specification alignment details")
        
        # 4. Check for diversity in matches
        unique_voltages = set()
        unique_sizes = set()
        for match in matches:
            if match.specification_alignment:
                unique_voltages.add(match.specification_alignment.get("voltage"))
                unique_sizes.add(match.specification_alignment.get("conductor_size"))
        
        if len(unique_voltages) > 2:
            warnings.append("Matches span multiple voltage levels - verify requirements")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "best_match_score": best_score,
            "average_match_score": avg_score,
            "match_count": len(matches),
            "recommendation": "GOOD" if best_score >= 0.85 else "ACCEPTABLE" if best_score >= 0.70 else "POOR"
        }
    
    def validate_pricing(
        self,
        rfp: RFPSummary,
        pricing: PricingBreakdown,
        historical_prices: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Validate pricing for anomalies and competitiveness
        
        Args:
            rfp: RFP being priced
            pricing: Pricing breakdown
            historical_prices: Historical prices for comparison
            
        Returns:
            Pricing validation report
        """
        logger.info(f"Validating pricing for RFP {rfp.rfp_id}")
        
        issues = []
        warnings = []
        anomalies = []
        
        # 1. Basic sanity checks
        if pricing.total <= 0:
            issues.append("Total price is zero or negative")
        
        if pricing.unit_price <= 0:
            issues.append("Unit price is zero or negative")
        
        # 2. Component validation
        expected_subtotal = pricing.unit_price * pricing.quantity
        if abs(pricing.subtotal - expected_subtotal) > 1:  # Allow 1 rupee difference for rounding
            issues.append(
                f"Subtotal mismatch: {pricing.subtotal} != {expected_subtotal} "
                f"(unit_price * quantity)"
            )
        
        # 3. Testing cost validation
        if pricing.testing_cost:
            testing_percentage = (pricing.testing_cost / pricing.subtotal) * 100
            if testing_percentage > 15:
                warnings.append(
                    f"Testing cost is high ({testing_percentage:.1f}% of subtotal)"
                )
        
        # 4. Delivery cost validation
        if pricing.delivery_cost:
            delivery_percentage = (pricing.delivery_cost / pricing.subtotal) * 100
            if delivery_percentage > 10:
                warnings.append(
                    f"Delivery cost is high ({delivery_percentage:.1f}% of subtotal)"
                )
        
        # 5. Historical comparison
        if historical_prices and len(historical_prices) > 0:
            avg_historical = sum(historical_prices) / len(historical_prices)
            deviation = abs(pricing.unit_price - avg_historical) / avg_historical
            
            if deviation > self.compliance_rules["max_price_deviation"]:
                anomalies.append(
                    f"Price deviates {deviation*100:.1f}% from historical average "
                    f"(₹{avg_historical:.2f})"
                )
                
                if pricing.unit_price > avg_historical * 1.3:
                    warnings.append("Price significantly higher than historical average")
                elif pricing.unit_price < avg_historical * 0.7:
                    warnings.append("Price significantly lower than historical average - verify costs")
        
        # 6. Total calculation validation
        expected_total = (
            pricing.subtotal +
            (pricing.testing_cost or 0) +
            (pricing.delivery_cost or 0) +
            (pricing.urgency_adjustment or 0)
        )
        
        if abs(pricing.total - expected_total) > 1:
            issues.append(
                f"Total calculation error: {pricing.total} != {expected_total}"
            )
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "anomalies": anomalies,
            "price_level": self._classify_price_level(pricing, historical_prices),
            "recommendation": "APPROVE" if len(issues) == 0 and len(anomalies) == 0 else "REVIEW"
        }
    
    def _check_completeness(self, rfp: RFPSummary) -> Dict[str, Any]:
        """Check if RFP has all required information"""
        issues = []
        
        if not rfp.title or len(rfp.title.strip()) < 10:
            issues.append("RFP title is missing or too short")
        
        if not rfp.scope or len(rfp.scope.strip()) < 20:
            issues.append("RFP scope is missing or insufficient")
        
        if not rfp.deadline:
            issues.append("Deadline is missing")
        
        if not rfp.source:
            issues.append("Source information is missing")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "completeness_score": 1.0 - (len(issues) * 0.25)
        }
    
    def _check_deadline(self, rfp: RFPSummary) -> Dict[str, Any]:
        """Validate deadline is reasonable"""
        if not rfp.deadline:
            return {
                "passed": False,
                "severity": "critical",
                "message": "No deadline specified"
            }
        
        days_remaining = (rfp.deadline - datetime.now()).days
        
        if days_remaining < 0:
            return {
                "passed": False,
                "severity": "critical",
                "message": f"Deadline has passed ({abs(days_remaining)} days ago)"
            }
        
        if days_remaining < self.compliance_rules["min_deadline_days"]:
            return {
                "passed": False,
                "severity": "critical",
                "message": f"Deadline too soon ({days_remaining} days remaining)"
            }
        
        if days_remaining > 180:
            return {
                "passed": True,
                "severity": "warning",
                "message": f"Deadline is very far ({days_remaining} days)"
            }
        
        return {
            "passed": True,
            "severity": "none",
            "message": f"Deadline is acceptable ({days_remaining} days remaining)"
        }
    
    def _check_specifications(self, rfp: RFPSummary) -> Dict[str, Any]:
        """Validate technical specifications"""
        issues = []
        
        if not rfp.specifications:
            issues.append("No specifications provided")
            return {"passed": False, "issues": issues}
        
        # Check for required specifications
        for required_spec in self.compliance_rules["required_specs"]:
            if required_spec not in rfp.specifications:
                issues.append(f"Missing required specification: {required_spec}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _check_testing_requirements(self, rfp: RFPSummary) -> Dict[str, Any]:
        """Validate testing requirements"""
        warnings = []
        
        if not rfp.testing_requirements or len(rfp.testing_requirements) == 0:
            warnings.append("No testing requirements specified")
        
        return {
            "passed": True,  # Not critical
            "warnings": warnings
        }
    
    def _calculate_compliance_score(self, checks: Dict[str, Any]) -> float:
        """Calculate overall compliance score"""
        scores = []
        
        if "completeness" in checks:
            scores.append(checks["completeness"].get("completeness_score", 0))
        
        if "deadline" in checks:
            scores.append(1.0 if checks["deadline"]["passed"] else 0.0)
        
        if "specifications" in checks:
            scores.append(1.0 if checks["specifications"]["passed"] else 0.5)
        
        if "testing" in checks:
            scores.append(1.0 if checks["testing"]["passed"] else 0.8)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _classify_price_level(
        self,
        pricing: PricingBreakdown,
        historical_prices: Optional[List[float]]
    ) -> str:
        """Classify price as aggressive, competitive, or conservative"""
        if not historical_prices or len(historical_prices) == 0:
            return "UNKNOWN"
        
        avg_historical = sum(historical_prices) / len(historical_prices)
        
        if pricing.unit_price < avg_historical * 0.90:
            return "AGGRESSIVE"
        elif pricing.unit_price < avg_historical * 1.05:
            return "COMPETITIVE"
        else:
            return "CONSERVATIVE"
    
    def generate_audit_report(
        self,
        rfp: RFPSummary,
        matches: List[ProductMatch],
        pricing: PricingBreakdown
    ) -> Dict[str, Any]:
        """
        Generate comprehensive audit report
        
        Args:
            rfp: RFP being audited
            matches: Product matches
            pricing: Pricing breakdown
            
        Returns:
            Complete audit report
        """
        logger.info(f"Generating audit report for RFP {rfp.rfp_id}")
        
        rfp_validation = self.validate_rfp(rfp)
        match_validation = self.validate_matches(rfp, matches)
        pricing_validation = self.validate_pricing(rfp, pricing)
        
        # Overall recommendation
        all_passed = (
            rfp_validation["is_compliant"] and
            match_validation["passed"] and
            pricing_validation["passed"]
        )
        
        critical_issues = (
            len(rfp_validation["issues"]) +
            len(match_validation["issues"]) +
            len(pricing_validation["issues"])
        )
        
        if all_passed:
            overall_recommendation = "APPROVE"
        elif critical_issues > 5:
            overall_recommendation = "REJECT"
        else:
            overall_recommendation = "REVIEW"
        
        return {
            "rfp_id": rfp.rfp_id,
            "audit_timestamp": datetime.now().isoformat(),
            "auditor_version": self.version,
            "rfp_validation": rfp_validation,
            "match_validation": match_validation,
            "pricing_validation": pricing_validation,
            "overall_recommendation": overall_recommendation,
            "critical_issues_count": critical_issues,
            "summary": self._generate_summary(
                rfp_validation,
                match_validation,
                pricing_validation
            )
        }
    
    def _generate_summary(
        self,
        rfp_val: Dict,
        match_val: Dict,
        pricing_val: Dict
    ) -> str:
        """Generate human-readable summary"""
        parts = []
        
        if rfp_val["is_compliant"]:
            parts.append("RFP is compliant")
        else:
            parts.append(f"RFP has {len(rfp_val['issues'])} compliance issues")
        
        if match_val["passed"]:
            parts.append(f"Product matches are {match_val['recommendation'].lower()}")
        else:
            parts.append("Product matches need review")
        
        if pricing_val["passed"]:
            parts.append(f"Pricing is {pricing_val.get('price_level', 'acceptable').lower()}")
        else:
            parts.append("Pricing has issues")
        
        return ". ".join(parts) + "."
