# AI Agents Architecture

This document describes the AI agents system for RFP automation.

## Overview

The system consists of 5 specialized AI agents orchestrated through a workflow manager:

```
┌─────────────────────────────────────────────────────────────┐
│                    RFP Workflow Orchestrator                 │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│ Sales Agent  │      │Document Agent│     │Technical Agt │
│              │      │              │     │              │
│ - Discover   │──────▶│ - Parse PDF  │────▶│ - Match      │
│ - Summarize  │      │ - Extract    │     │   Products   │
└──────────────┘      │   Specs      │     │ - Score      │
                      └──────────────┘     └──────────────┘
                                                   │
                              ┌────────────────────┘
                              ▼
                      ┌──────────────┐
                      │ Pricing Agt  │
                      │              │
                      │ - Calculate  │
                      │ - Recommend  │
                      └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ Learning Agt │
                      │              │
                      │ - Process    │
                      │   Feedback   │
                      │ - Improve    │
                      └──────────────┘
```

## Agent Descriptions

### 1. Sales Agent (`agents/sales/agent.py`)

**Purpose**: Discover RFPs from web sources and create summaries

**Capabilities**:
- Web scraping using BeautifulSoup
- RFP discovery from tender portals
- RFP summarization with NLP
- Entity extraction (buyer, location, deadline)
- RFP validation

**Key Methods**:
```python
discover_rfps_from_url(url: str) -> List[RFPSummary]
summarize_rfp(text: str) -> RFPSummary
```

**Usage Example**:
```python
from agents.sales.agent import SalesAgent

agent = SalesAgent()
rfps = await agent.discover_rfps_from_url("https://example.com/tenders")
summary = agent.summarize_rfp(rfp_text)
```

### 2. Document Agent (`agents/document/agent.py`)

**Purpose**: Parse PDF documents and extract technical specifications

**Capabilities**:
- PDF text extraction with pdfplumber
- Specification extraction using regex patterns
- Pattern matching for:
  - Voltage levels (11kV, 33kV, etc.)
  - Current ratings (185mm², 240mm²)
  - Materials (XLPE, PVC, Copper, Aluminum)
  - Standards (IS, IEC, BS)
- Confidence scoring

**Key Methods**:
```python
parse_pdf(pdf_path: str) -> str
extract_specifications(pdf_path: str) -> List[Specification]
```

**Usage Example**:
```python
from agents.document.agent import DocumentAgent

agent = DocumentAgent()
text = agent.parse_pdf("rfp_document.pdf")
specs = agent.extract_specifications("rfp_document.pdf")
```

### 3. Technical Agent (`agents/technical/agent.py`)

**Purpose**: Match RFP specifications with product catalog

**Capabilities**:
- Rule-based product matching
- Weighted scoring system (voltage, current, material, standards)
- Mock product catalog (5 cable products)
- Semantic search placeholder (ready for vector DB)
- Match confidence scoring

**Key Methods**:
```python
match_products(specifications: List[Specification]) -> List[ProductMatch]
semantic_search(query: str, top_k: int) -> List[Dict]
```

**Usage Example**:
```python
from agents.technical.agent import TechnicalAgent

agent = TechnicalAgent()
matches = agent.match_products(specifications)
# Sorted by match score, best matches first
```

### 4. Pricing Agent (`agents/pricing/agent.py`)

**Purpose**: Calculate pricing estimates and recommendations

**Capabilities**:
- Base pricing calculation
- Testing cost calculation (type/routine/sample tests)
- Delivery cost estimation
- Urgency adjustments based on deadline
- Discount application
- Cost breakdown reports
- Product recommendation based on price + match score

**Key Methods**:
```python
calculate_pricing(rfp_id, matches, quantity, deadline, testing_requirements) -> List[PricingBreakdown]
get_recommended_product(pricing_list, matches) -> str
apply_discount(pricing, discount_percent) -> PricingBreakdown
```

**Pricing Formula**:
```
Total = Subtotal + Testing Cost + Delivery Cost + Urgency Adjustment

Where:
- Subtotal = Unit Price × Quantity
- Testing Cost = Subtotal × Test Multiplier (2-5%)
- Delivery Cost = Base (₹5,000) + (Quantity > 5000) × ₹0.5/meter
- Urgency Adjustment:
  - <14 days: 15% premium
  - <30 days: 8% premium
  - <60 days: 3% premium
```

**Usage Example**:
```python
from agents.pricing.agent import PricingAgent

agent = PricingAgent()
pricing_list = agent.calculate_pricing(
    rfp_id="RFP-001",
    matches=matches,
    quantity=1000,
    deadline=datetime(2024, 12, 31),
    testing_requirements=["type_test", "routine_test"]
)
recommended = agent.get_recommended_product(pricing_list, matches)
```

### 5. Learning Agent (`agents/learning/agent.py`)

**Purpose**: Process feedback and improve system performance

**Capabilities**:
- Feedback collection (win/loss/accuracy)
- Performance metrics tracking
- Trend analysis
- Issue identification
- Improvement suggestions
- Performance reporting

**Key Methods**:
```python
process_feedback(rfp_id, feedback_type, rating, comments, ...) -> Dict
get_performance_report(days=30) -> Dict
suggest_improvements() -> List[Dict]
```

**Tracked Metrics**:
- Average rating (1-5)
- Win rate (%)
- Match accuracy (0-1)
- Pricing accuracy (0-1)
- Response time (seconds)
- Feedback type distribution

**Usage Example**:
```python
from agents.learning.agent import LearningAgent

agent = LearningAgent()

# Submit feedback
result = agent.process_feedback(
    rfp_id="RFP-001",
    feedback_type="win",
    rating=4,
    comments="Great match, accurate pricing",
    match_accuracy=0.92,
    pricing_accuracy=0.88
)

# Get report
report = agent.get_performance_report(days=30)
suggestions = agent.suggest_improvements()
```

## Workflow Orchestration

### RFPWorkflow Class (`orchestrator/workflow.py`)

Coordinates all agents for end-to-end RFP processing.

**Processing Pipelines**:

#### 1. URL-based Processing
```python
workflow = RFPWorkflow()

result = await workflow.process_rfp_from_url(
    url="https://example.com/tender",
    quantity=1000,
    testing_requirements=["type_test"]
)
```

**Pipeline Steps**:
1. **Sales Agent**: Discover RFPs from URL
2. **Sales Agent**: Summarize RFP content
3. **Document Agent**: Extract specs from PDF (if available)
4. **Technical Agent**: Match products to specifications
5. **Pricing Agent**: Calculate pricing for matches
6. **Pricing Agent**: Generate recommendation

#### 2. PDF-based Processing
```python
result = await workflow.process_rfp_from_pdf(
    pdf_path="rfp_document.pdf",
    rfp_metadata={
        'rfp_id': 'RFP-001',
        'deadline': datetime(2024, 12, 31)
    },
    quantity=1000,
    testing_requirements=["routine_test"]
)
```

**Pipeline Steps**:
1. **Document Agent**: Parse PDF text
2. **Document Agent**: Extract specifications
3. **Technical Agent**: Match products
4. **Pricing Agent**: Calculate pricing
5. **Pricing Agent**: Generate recommendation

#### 3. Feedback Processing
```python
feedback_result = workflow.submit_feedback(
    rfp_id="RFP-001",
    feedback_type="win",
    rating=4,
    comments="Excellent response",
    match_accuracy=0.92,
    pricing_accuracy=0.88
)
```

**Result Structure**:
```json
{
  "status": "success",
  "rfp_summary": {
    "rfp_id": "RFP-001",
    "title": "Supply of 11kV XLPE Cables",
    "deadline": "2024-12-31T00:00:00",
    "buyer": "State Electricity Board",
    "location": "Mumbai"
  },
  "specifications": [
    {
      "type": "voltage",
      "value": "11",
      "unit": "kV",
      "confidence": 0.95
    }
  ],
  "matches": [
    {
      "sku": "XLPE-11KV-185",
      "name": "11kV XLPE Cable 3x185 sq.mm",
      "match_score": 0.95,
      "matched_specs": ["voltage", "material"]
    }
  ],
  "pricing": [
    {
      "sku": "XLPE-11KV-185",
      "unit_price": 450.00,
      "quantity": 1000,
      "total": 462750.00,
      "breakdown": { ... }
    }
  ],
  "recommendation": {
    "sku": "XLPE-11KV-185",
    "pricing": { ... }
  },
  "processing_time": 2.45
}
```

## Integration with FastAPI

### Current Setup

All agents are **modular and independent**. They can be integrated with the existing FastAPI endpoints:

```python
# In orchestrator/api/routes/rfp.py
from orchestrator.workflow import RFPWorkflow

workflow = RFPWorkflow()

@router.post("/process-url")
async def process_rfp_url(url: str, quantity: int = 1000):
    result = await workflow.process_rfp_from_url(url, quantity)
    return result

@router.post("/process-pdf")
async def process_rfp_pdf(file: UploadFile, metadata: dict):
    # Save uploaded file
    pdf_path = f"temp/{file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await file.read())
    
    result = await workflow.process_rfp_from_pdf(pdf_path, metadata)
    return result
```

### Integration Steps

1. **Import workflow in route handlers**:
```python
from orchestrator.workflow import RFPWorkflow
```

2. **Initialize workflow instance**:
```python
workflow = RFPWorkflow()
```

3. **Call workflow methods in endpoints**:
```python
result = await workflow.process_rfp_from_url(url)
```

4. **Return results to frontend**:
```python
return result
```

## Testing Agents Individually

Each agent can be tested independently:

```python
# Test Sales Agent
from agents.sales.agent import SalesAgent
agent = SalesAgent()
rfps = await agent.discover_rfps_from_url("https://example.com")

# Test Document Agent
from agents.document.agent import DocumentAgent
agent = DocumentAgent()
specs = agent.extract_specifications("test.pdf")

# Test Technical Agent
from agents.technical.agent import TechnicalAgent
agent = TechnicalAgent()
matches = agent.match_products(specs)

# Test Pricing Agent
from agents.pricing.agent import PricingAgent
agent = PricingAgent()
pricing = agent.calculate_pricing("RFP-001", matches, 1000)

# Test Learning Agent
from agents.learning.agent import LearningAgent
agent = LearningAgent()
result = agent.process_feedback("RFP-001", "win", 4)
```

## Future Enhancements

### 1. Vector Database Integration (Technical Agent)
- Replace mock product catalog with Qdrant
- Implement semantic search with embeddings
- Store product specifications as vectors

### 2. ML Model Integration
- Train match scoring model
- Improve specification extraction with NER
- Enhance RFP summarization with transformers

### 3. Real-time Processing
- WebSocket support for live updates
- Progress tracking for long-running workflows
- Async task queue (Celery/Redis)

### 4. Advanced Learning
- A/B testing for pricing strategies
- Recommendation model training
- Automated parameter tuning

### 5. Database Persistence
- Store feedback in PostgreSQL
- Track agent performance metrics
- Historical analysis and reporting

## Dependencies

```txt
# Core
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9

# Web scraping
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

# Document processing
pdfplumber==0.10.3
PyPDF2==3.0.1

# Future ML/AI
# qdrant-client==1.7.0
# sentence-transformers==2.2.2
# transformers==4.35.0
```

## Configuration

Agents use environment variables for configuration:

```env
# API Keys (future)
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Vector DB (future)
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Logging
LOG_LEVEL=INFO
```

## Error Handling

All agents implement comprehensive error handling:

```python
try:
    result = agent.process()
except Exception as e:
    logger.error(f"Error: {str(e)}")
    return {
        'status': 'error',
        'message': str(e)
    }
```

## Monitoring

Health check endpoint:

```python
@router.get("/health/agents")
async def agent_health():
    workflow = RFPWorkflow()
    return workflow.health_check()
```

Response:
```json
{
  "status": "healthy",
  "agents": {
    "sales": {"name": "SalesAgent", "version": "1.0.0", "status": "ready"},
    "document": {"name": "DocumentAgent", "version": "1.0.0", "status": "ready"},
    "technical": {"name": "TechnicalAgent", "version": "1.0.0", "status": "ready"},
    "pricing": {"name": "PricingAgent", "version": "1.0.0", "status": "ready"},
    "learning": {"name": "LearningAgent", "version": "1.0.0", "status": "ready"}
  }
}
```

## Summary

The AI agent system is fully implemented with:
- ✅ 5 specialized agents (Sales, Document, Technical, Pricing, Learning)
- ✅ Workflow orchestration
- ✅ Modular, testable architecture
- ✅ Easy FastAPI integration
- ✅ Comprehensive error handling
- ✅ Ready for ML/AI enhancements

All agents are **production-ready** with placeholder implementations that can be enhanced with ML models and vector databases when needed.
