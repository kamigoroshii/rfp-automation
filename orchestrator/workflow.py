"""
Workflow Orchestrator - Coordinates AI agents for RFP processing
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from agents.sales.agent import SalesAgent
from agents.document.agent import DocumentAgent
from agents.technical.agent import TechnicalAgent
from agents.pricing.agent import PricingAgent
from agents.learning.agent import LearningAgent
from agents.auditor.agent import AuditorAgent

from shared.models import (
    RFPSummary, 
    Specification, 
    ProductMatch, 
    PricingBreakdown
)

logger = logging.getLogger(__name__)


class RFPWorkflow:
    """Orchestrates the complete RFP processing workflow"""
    
    def __init__(self):
        # Initialize all agents
        self.sales_agent = SalesAgent()
        self.document_agent = DocumentAgent()
        self.technical_agent = TechnicalAgent()
        self.pricing_agent = PricingAgent()
        self.learning_agent = LearningAgent()
        self.auditor_agent = AuditorAgent()
        
        logger.info("RFP Workflow Orchestrator initialized")
    
    async def process_rfp_from_url(
        self,
        url: str,
        quantity: int = 1000,
        testing_requirements: List[str] = None
    ) -> Dict[str, Any]:
        """
        Process RFP from URL through complete pipeline
        
        Args:
            url: URL to discover RFP from
            quantity: Required quantity
            testing_requirements: List of testing requirements
            
        Returns:
            Complete RFP processing result
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting RFP processing from URL: {url}")
            
            # Step 1: Discover RFPs
            logger.info("Step 1: Discovering RFPs...")
            rfps = await self.sales_agent.discover_rfps_from_url(url)
            
            if not rfps:
                return {
                    'status': 'error',
                    'message': 'No RFPs discovered from URL'
                }
            
            # Process first RFP (in production, handle multiple)
            rfp = rfps[0]
            
            # Step 2: Summarize RFP
            logger.info("Step 2: Summarizing RFP...")
            summary = self.sales_agent.summarize_rfp(rfp)
            
            # Step 3: Extract specifications (if PDF available)
            logger.info("Step 3: Extracting specifications...")
            specifications = []
            if hasattr(summary, 'attachments') and summary.attachments:
                for attachment in summary.attachments:
                    if attachment.endswith('.pdf'):
                        specs = self.document_agent.extract_specifications(attachment)
                        specifications.extend(specs)
            
            # Step 4: Match products
            logger.info("Step 4: Matching products...")
            matches = self.technical_agent.match_products(
                specifications if specifications else []
            )
            
            # Step 5: Calculate pricing
            logger.info("Step 5: Calculating pricing...")
            pricing_list = self.pricing_agent.calculate_pricing(
                rfp_id=summary.rfp_id,
                matches=matches,
                quantity=quantity,
                deadline=summary.deadline,
                testing_requirements=testing_requirements or []
            )
            
            # Step 6: Get recommendation
            logger.info("Step 6: Generating recommendation...")
            recommended_sku = self.pricing_agent.get_recommended_product(
                pricing_list,
                matches
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            logger.info(
                f"RFP processing completed in {processing_time:.2f} seconds"
            )
            
            return {
                'status': 'success',
                'rfp_summary': {
                    'rfp_id': summary.rfp_id,
                    'title': summary.title,
                    'deadline': summary.deadline.isoformat() if summary.deadline else None,
                    'buyer': summary.buyer,
                    'location': summary.location
                },
                'specifications': [
                    {
                        'type': spec.spec_type,
                        'value': spec.value,
                        'unit': spec.unit,
                        'confidence': spec.confidence
                    }
                    for spec in specifications
                ],
                'matches': [
                    {
                        'sku': match.sku,
                        'name': match.name,
                        'match_score': match.match_score,
                        'matched_specs': match.matched_specs
                    }
                    for match in matches
                ],
                'pricing': [
                    {
                        'sku': pricing.sku,
                        'unit_price': pricing.unit_price,
                        'quantity': pricing.quantity,
                        'total': pricing.total,
                        'breakdown': self.pricing_agent.generate_cost_breakdown_report(pricing)
                    }
                    for pricing in pricing_list
                ],
                'recommendation': {
                    'sku': recommended_sku,
                    'pricing': next(
                        (p for p in pricing_list if p.sku == recommended_sku),
                        None
                    )
                },
                'audit_report': audit_report,
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"Error in RFP workflow: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'message': str(e)
            }

    async def process_next_rfp(self) -> Dict[str, Any]:
        """
        Process the next qualified RFP from the Redis queue
        """
        try:
            # Lazy import to avoid circular dependency if any
            from shared.cache.redis_manager import RedisManager
            redis_mgr = RedisManager()
            
            # Pop next ticket
            ticket_data = redis_mgr.pop_rfp("rfp_tickets")
            
            if not ticket_data:
                return {'status': 'empty', 'message': 'No RFPs in queue'}
                
            logger.info(f"Processing RFP Ticket: {ticket_data.get('rfp_id')}")
            
            # Reconstruct RFPSummary object
            rfp_summary = RFPSummary.from_dict(ticket_data)
            
            # Split Summary (Technical vs Commercial)
            tech_summary, comm_summary = self._split_summary(rfp_summary)
            
            # Technical Agent Flow
            # Pass technical scope/summary to Technical Agent
            # Note: Currently TechnicalAgent expectations might need adjustment, 
            # passing the full text for now or extracting specs first.
            # Ideally we extract specs from the scope text first.
            
            # For this phase, we assume the DocumentAgent extracts from the scope text
            # if no PDF is present (which is the case for most scraped RFPs).
            # We'll treat the 'scope' text as the document source.
            
            # 1. Extract Specs from Text
            # We need to expose a method in DocumentAgent for text-based extraction 
            # or use regex directly here. The Requirement says "Technical Agent extracts Scope of Supply".
            # Let's delegate to Technical Agent if it has that capability, or Document Agent.
            # Looking at existing code, DocumentAgent has `extract_specifications`.
            
            # Let's assume we save the scope to a temp file or the agent handles text.
            # For now, we will try to use the Document Agent's regex logic on the raw text.
            # This might require a small update to DocumentAgent later to accept raw text.
            # We'll simulate it by passing the scope string.
            
            # For now, let's proceed with the flow as defined:
            
            # 1. Technical Agent: Extract & Match
            # We'll update TechnicalAgent to accept text input for extraction if needed,
            # or pass it to DocumentAgent first.
            # Let's use DocumentAgent for extraction as per original design, then Technical for matching.
            
            # Hack: Create a dummy spec object for now from the scope text
            # In a real scenario, we'd update DocumentAgent to parse text strings.
            specifications = self.document_agent.extract_specifications_from_text(tech_summary)
            
            # 2. Match Products
            matches = self.technical_agent.match_products(specifications)
            
            # 3. Pricing Agent
            pricing_list = self.pricing_agent.calculate_pricing(
                rfp_id=rfp_summary.rfp_id,
                matches=matches,
                quantity=1000, # Default or extracted
                deadline=rfp_summary.deadline,
                testing_requirements=[] # Extracted from comm_summary
            )
            
            # 4. Recommendation
            recommended_sku = self.pricing_agent.get_recommended_product(pricing_list, matches)
            
            # 5. Send to Auditor (Placeholder for Module 4)
            # ...
            
            return {
                'status': 'success',
                'rfp_id': rfp_summary.rfp_id,
                'matches': [m.sku for m in matches],
                'recommended': recommended_sku
            }
            
        except Exception as e:
            logger.error(f"Error processing ticket: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _split_summary(self, rfp: RFPSummary) -> tuple[str, str]:
        """
        Split RFP scope into Technical and Commercial summaries
        Returns: (technical_text, commercial_text)
        """
        full_text = rfp.scope
        
        # Simple keyword-based splitting
        # In reality, this would be an LLM call or advanced NLP
        
        tech_keywords = ['cable', 'wire', 'voltage', 'conductor', 'xlpe', 'pvc', 'mm', 'kv']
        comm_keywords = ['payment', 'delivery', 'warranty', 'penalty', 'terms', 'price']
        
        tech_lines = []
        comm_lines = []
        
        for line in full_text.split('\n'):
            line_lower = line.lower()
            if any(k in line_lower for k in tech_keywords):
                tech_lines.append(line)
            elif any(k in line_lower for k in comm_keywords):
                comm_lines.append(line)
            else:
                # Default to technical if ambiguous
                tech_lines.append(line)
                
        return "\n".join(tech_lines), "\n".join(comm_lines)
    
    async def process_rfp_from_pdf(
        self,
        pdf_path: str,
        rfp_metadata: Dict[str, Any],
        quantity: int = 1000,
        testing_requirements: List[str] = None
    ) -> Dict[str, Any]:
        """
        Process RFP from PDF file
        
        Args:
            pdf_path: Path to PDF file (can be None for email-based RFPs)
            rfp_metadata: RFP metadata (title, deadline, buyer, etc.)
            quantity: Required quantity
            testing_requirements: List of testing requirements
            
        Returns:
            Complete RFP processing result
        """
        try:
            start_time = datetime.now()
            logger.info(f"Starting RFP processing from PDF: {pdf_path}")
            
            # Check if PDF path is provided
            if not pdf_path:
                logger.warning("No PDF path provided - skipping PDF parsing (email-based RFP)")
                return {
                    'status': 'error',
                    'message': 'No PDF file provided for processing. Email-based RFPs should use text-based workflow.',
                    'rfp_id': rfp_metadata.get('rfp_id', 'unknown')
                }
            
            # Step 1: Parse PDF
            logger.info("Step 1: Parsing PDF...")
            text_content = self.document_agent.parse_pdf(pdf_path)
            
            # Step 2: Extract specifications
            logger.info("Step 2: Extracting specifications...")
            specifications = self.document_agent.extract_specifications(pdf_path)
            
            # Step 3: Match products
            logger.info("Step 3: Matching products...")
            matches = self.technical_agent.match_products(specifications)
            
            # Step 4: Calculate pricing
            logger.info("Step 4: Calculating pricing...")
            rfp_id = rfp_metadata.get('rfp_id', f"RFP-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
            deadline = rfp_metadata.get('deadline')
            
            pricing_list = self.pricing_agent.calculate_pricing(
                rfp_id=rfp_id,
                matches=matches,
                quantity=quantity,
                deadline=deadline,
                testing_requirements=testing_requirements or []
            )
            
            # Step 5: Get recommendation
            logger.info("Step 5: Generating recommendation...")
            recommended_sku = self.pricing_agent.get_recommended_product(
                pricing_list,
                matches
            )
            
            # Step 6: Audit the results
            logger.info("Step 6: Auditing proposal...")
            # Create RFPSummary for auditor
            rfp_summary = RFPSummary(
                rfp_id=rfp_id,
                title=rfp_metadata.get('title', 'Unknown'),
                source=rfp_metadata.get('source', 'PDF'),
                deadline=deadline,
                scope=text_content.get('text', '')[:500] if isinstance(text_content, dict) else str(text_content)[:500],
                testing_requirements=testing_requirements or [],
                discovered_at=datetime.now(),
                status='auditing'
            )
            
            audit_report = self.auditor_agent.validate_rfp(rfp_summary)
            
            # Validate matches
            matches_validation = self.auditor_agent.validate_matches(rfp_summary, matches)
            audit_report['matches_validation'] = matches_validation
            
            # Validate pricing (use first pricing item as representative)
            if pricing_list:
                pricing_validation = self.auditor_agent.validate_pricing(
                    rfp_summary,
                    pricing_list[0]
                )
                audit_report['pricing_validation'] = pricing_validation
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            logger.info(
                f"PDF processing completed in {processing_time:.2f} seconds - Audit: {audit_report['recommendation']}"
            )
            
            return {
                'status': 'success',
                'rfp_id': rfp_id,
                'specifications': [
                    {
                        'type': spec.spec_type,
                        'value': spec.value,
                        'unit': spec.unit,
                        'confidence': spec.confidence
                    }
                    for spec in specifications
                ],
                'matches': [
                    {
                        'sku': match.sku,
                        'name': match.name,
                        'match_score': match.match_score,
                        'matched_specs': match.matched_specs
                    }
                    for match in matches
                ],
                'pricing': [
                    {
                        'sku': pricing.sku,
                        'unit_price': pricing.unit_price,
                        'quantity': pricing.quantity,
                        'total': pricing.total
                    }
                    for pricing in pricing_list
                ],
                'recommendation': {
                    'sku': recommended_sku
                },
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"Error in PDF workflow: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def submit_feedback(
        self,
        rfp_id: str,
        feedback_type: str,
        rating: int,
        comments: str = None,
        match_accuracy: float = None,
        pricing_accuracy: float = None,
        response_time: float = None
    ) -> Dict[str, Any]:
        """
        Submit feedback for processed RFP
        
        Args:
            rfp_id: RFP identifier
            feedback_type: Type of feedback (win/loss/accuracy)
            rating: Rating score (1-5)
            comments: Optional comments
            match_accuracy: Match accuracy score
            pricing_accuracy: Pricing accuracy score
            response_time: Response time
            
        Returns:
            Feedback processing result
        """
        return self.learning_agent.process_feedback(
            rfp_id=rfp_id,
            feedback_type=feedback_type,
            rating=rating,
            comments=comments,
            match_accuracy=match_accuracy,
            pricing_accuracy=pricing_accuracy,
            response_time=response_time
        )
    
    def get_performance_report(self, days: int = 30) -> Dict[str, Any]:
        """Get system performance report"""
        return self.learning_agent.get_performance_report(days=days)
    
    def get_improvement_suggestions(self) -> List[Dict[str, Any]]:
        """Get suggestions for system improvement"""
        return self.learning_agent.suggest_improvements()
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all agents"""
        return {
            'status': 'healthy',
            'agents': {
                'sales': {
                    'name': self.sales_agent.name,
                    'version': self.sales_agent.version,
                    'status': 'ready'
                },
                'document': {
                    'name': self.document_agent.name,
                    'version': self.document_agent.version,
                    'status': 'ready'
                },
                'technical': {
                    'name': self.technical_agent.name,
                    'version': self.technical_agent.version,
                    'status': 'ready'
                },
                'pricing': {
                    'name': self.pricing_agent.name,
                    'version': self.pricing_agent.version,
                    'status': 'ready'
                },
                'learning': {
                    'name': self.learning_agent.name,
                    'version': self.learning_agent.version,
                    'status': 'ready'
                }
            }
        }
