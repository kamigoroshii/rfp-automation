# Design Document

## Overview

The RFP Automation System is a microservices-based multi-agent AI platform that automates the complete RFP response lifecycle. The architecture follows an agent-based design pattern where autonomous agents (Sales, Document, Technical, Pricing, Learning) are coordinated by a central Orchestrator using the CrewAI framework. The system integrates web scraping, NLP, semantic search, machine learning, and REST APIs to provide an end-to-end solution.

### Key Design Principles

- **Agent Autonomy**: Each agent operates independently with defined inputs, outputs, and responsibilities
- **Asynchronous Processing**: Parallel execution of independent tasks for optimal performance
- **Scalability**: Containerized microservices architecture supporting horizontal scaling
- **Extensibility**: Modular design allowing easy addition of new agents or data sources
- **Data-Driven Learning**: Continuous improvement through feedback loops and model retraining

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Dashboard                        │
│                    (React.js + Olive Green UI)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent (CrewAI)                   │
│                         FastAPI Server                           │
└─┬───────────┬───────────┬───────────┬───────────┬──────────────┘
  │           │           │           │           │
  ▼           ▼           ▼           ▼           ▼
┌────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐
│ Sales  │ │ Document │ │Technical │ │ Pricing │ │ Learning │
│ Agent  │ │  Agent   │ │  Agent   │ │  Agent  │ │  Agent   │
└───┬────┘ └────┬─────┘ └────┬─────┘ └────┬────┘ └────┬─────┘
    │           │            │            │           │
    └───────────┴────────────┴────────────┴───────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Shared Memory Layer                         │
│              Redis (Cache) + PostgreSQL (Structured)             │
│                    + Qdrant (Vector Store)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.10+
- CrewAI (agent orchestration)
- FastAPI (REST API framework)
- Celery + Redis (async task queue)
- PostgreSQL (relational database)
- Qdrant (vector database)

**AI/ML:**
- HuggingFace Transformers (sentence-transformers/all-MiniLM-L6-v2)
- spaCy (NLP parsing)
- scikit-learn, XGBoost (pricing models)
- PyMuPDF, pdfplumber (PDF parsing)

**Web Scraping:**
- Requests + BeautifulSoup (static sites)
- Selenium (dynamic sites)
- IMAP (email integration)

**Frontend:**
- React.js 18+
- Axios (API client)
- Chart.js (analytics visualization)
- Tailwind CSS (olive green theme)

**DevOps:**
- Docker + Docker Compose
- GitHub Actions (CI/CD)
- AWS/GCP/Azure (cloud deployment)

## Components and Interfaces

### 1. Sales Agent

**Responsibility:** Discover and summarize RFPs from websites and emails

**Components:**
- `WebScraper`: Scrapes RFP portals using BeautifulSoup/Selenium
- `EmailMonitor`: Monitors inbox via IMAP for RFP announcements
- `RFPParser`: Extracts title, deadline, scope, testing requirements
- `RFPSummarizer`: Creates structured JSON summaries

**Input:** 
- Configuration: List of URLs to monitor, email credentials
- Schedule: Cron-based polling intervals

**Output:**
```json
{
  "rfp_id": "RFP-2025-001",
  "title": "Supply of 11kV XLPE Cables",
  "source": "https://example.com/rfp",
  "deadline": "2025-12-15T17:00:00Z",
  "scope": "Supply of 5000m 11kV XLPE cables",
  "testing_requirements": ["IEC 60502", "Type test", "Routine test"],
  "discovered_at": "2025-11-09T10:30:00Z",
  "status": "new"
}
```

**Interface:**
```python
class SalesAgent:
    def discover_rfps(self) -> List[RFPSummary]
    def parse_rfp(self, source: str) -> RFPSummary
    def save_to_memory(self, rfp: RFPSummary) -> str
```

### 2. Document Agent

**Responsibility:** Parse PDF/text documents and extract specifications

**Components:**
- `PDFExtractor`: Extracts text and tables using PyMuPDF/pdfplumber
- `SpecificationParser`: Uses spaCy NER and regex patterns to identify specs
- `StructuredOutputGenerator`: Creates specification dictionaries

**Input:**
```json
{
  "rfp_id": "RFP-2025-001",
  "document_path": "/data/rfps/RFP-2025-001.pdf"
}
```

**Output:**
```json
{
  "rfp_id": "RFP-2025-001",
  "specifications": {
    "cable_type": "XLPE",
    "voltage_rating": "11kV",
    "conductor_material": "Aluminum",
    "conductor_size": "240 sq.mm",
    "insulation_type": "XLPE",
    "quantity": "5000m",
    "standards": ["IEC 60502-2", "IS 7098"]
  },
  "testing_requirements": {
    "type_tests": ["Partial discharge", "Impulse voltage"],
    "routine_tests": ["Conductor resistance", "Voltage test"],
    "certifications": ["BIS", "CPRI"]
  },
  "confidence_score": 0.92
}
```

**Interface:**
```python
class DocumentAgent:
    def extract_text(self, pdf_path: str) -> str
    def parse_specifications(self, text: str) -> Dict
    def validate_extraction(self, specs: Dict) -> float
```

### 3. Technical Agent

**Responsibility:** Match RFP specifications with product SKUs using semantic search

**Components:**
- `ProductDatabase`: Manages OEM product catalog
- `EmbeddingGenerator`: Creates semantic embeddings using sentence-transformers
- `VectorSearchEngine`: Queries Qdrant for similarity matches
- `MatchScorer`: Calculates match percentages and generates comparison tables

**Input:**
```json
{
  "rfp_id": "RFP-2025-001",
  "specifications": { /* from Document Agent */ }
}
```

**Output:**
```json
{
  "rfp_id": "RFP-2025-001",
  "matches": [
    {
      "sku": "XLPE-11KV-AL-240",
      "product_name": "11kV XLPE Aluminum Cable 240 sq.mm",
      "match_score": 0.94,
      "specification_alignment": {
        "voltage_rating": "exact_match",
        "conductor_material": "exact_match",
        "conductor_size": "exact_match",
        "insulation_type": "exact_match"
      },
      "datasheet_url": "https://oem.com/products/XLPE-11KV-AL-240.pdf"
    },
    {
      "sku": "XLPE-11KV-AL-300",
      "product_name": "11kV XLPE Aluminum Cable 300 sq.mm",
      "match_score": 0.87,
      "specification_alignment": {
        "voltage_rating": "exact_match",
        "conductor_material": "exact_match",
        "conductor_size": "close_match",
        "insulation_type": "exact_match"
      }
    }
  ],
  "comparison_table": "/* HTML/JSON table */"
}
```

**Interface:**
```python
class TechnicalAgent:
    def load_product_catalog(self, catalog_path: str) -> None
    def generate_embeddings(self, specs: Dict) -> np.ndarray
    def search_similar_products(self, embedding: np.ndarray, top_k: int) -> List[Match]
    def calculate_match_score(self, rfp_specs: Dict, product_specs: Dict) -> float
```

**Vector Database Schema (Qdrant):**
```python
{
  "collection_name": "product_catalog",
  "vector_size": 384,  # all-MiniLM-L6-v2 dimension
  "payload_schema": {
    "sku": "string",
    "product_name": "string",
    "specifications": "object",
    "datasheet_url": "string",
    "category": "string"
  }
}
```

### 4. Pricing Agent

**Responsibility:** Calculate cost estimates using rules and ML models

**Components:**
- `PricingDatabase`: Stores product prices, test costs, delivery rates
- `RuleEngine`: Applies rule-based pricing logic
- `MLPricingModel`: Uses XGBoost for dynamic pricing predictions
- `PricingCalculator`: Consolidates all cost components

**Input:**
```json
{
  "rfp_id": "RFP-2025-001",
  "matches": [ /* from Technical Agent */ ],
  "quantity": "5000m",
  "urgency": "standard",
  "delivery_location": "Mumbai"
}
```

**Output:**
```json
{
  "rfp_id": "RFP-2025-001",
  "pricing_breakdown": [
    {
      "sku": "XLPE-11KV-AL-240",
      "unit_price": 850.00,
      "quantity": 5000,
      "subtotal": 4250000.00,
      "testing_cost": 125000.00,
      "delivery_cost": 75000.00,
      "urgency_adjustment": 0.00,
      "total": 4450000.00,
      "currency": "INR"
    }
  ],
  "recommended_sku": "XLPE-11KV-AL-240",
  "total_estimate": 4450000.00,
  "confidence": 0.88
}
```

**Interface:**
```python
class PricingAgent:
    def load_pricing_tables(self) -> None
    def apply_rules(self, match: Match, quantity: int) -> float
    def predict_with_ml(self, features: Dict) -> float
    def calculate_total_cost(self, components: Dict) -> PricingBreakdown
```

**ML Model Features:**
```python
features = [
    'product_category',
    'quantity',
    'urgency_level',
    'delivery_distance',
    'testing_complexity',
    'historical_win_rate',
    'competitor_price_estimate'
]
```

### 5. Orchestrator Agent

**Responsibility:** Coordinate all agents using CrewAI and expose REST APIs

**Components:**
- `CrewManager`: Defines agent roles, goals, and tools using CrewAI
- `WorkflowEngine`: Manages sequential and parallel task execution
- `APIServer`: FastAPI endpoints for external integration
- `TaskQueue`: Celery for async processing

**CrewAI Configuration:**
```python
from crewai import Agent, Task, Crew

# Define agents
sales_agent = Agent(
    role='RFP Discovery Specialist',
    goal='Discover and summarize RFPs from multiple sources',
    tools=[web_scraper_tool, email_monitor_tool],
    memory=True
)

technical_agent = Agent(
    role='Product Matching Expert',
    goal='Match RFP specifications with product catalog',
    tools=[vector_search_tool, spec_comparison_tool],
    memory=True
)

pricing_agent = Agent(
    role='Pricing Analyst',
    goal='Calculate accurate cost estimates',
    tools=[pricing_calculator_tool, ml_model_tool],
    memory=True
)

# Define workflow
crew = Crew(
    agents=[sales_agent, technical_agent, pricing_agent],
    tasks=[discover_task, match_task, price_task],
    process='sequential'  # or 'parallel' for independent tasks
)
```

**REST API Endpoints:**
```python
# FastAPI routes
POST   /api/rfp/submit          # Submit new RFP for processing
GET    /api/rfp/{rfp_id}        # Get RFP status and results
GET    /api/rfp/list            # List all RFPs
POST   /api/rfp/{rfp_id}/feedback  # Submit outcome feedback
GET    /api/products/search     # Search product catalog
GET    /api/analytics/dashboard # Get dashboard metrics
```

**Interface:**
```python
class OrchestratorAgent:
    def initialize_crew(self) -> Crew
    def process_rfp(self, rfp_id: str) -> RFPResponse
    def execute_parallel_tasks(self, tasks: List[Task]) -> List[Result]
    def consolidate_results(self, results: Dict) -> RFPResponse
```

### 6. Learning Agent

**Responsibility:** Collect feedback and retrain models

**Components:**
- `FeedbackCollector`: Records submission outcomes
- `PerformanceTracker`: Calculates win rate, accuracy metrics
- `ModelRetrainer`: Retrains Technical and Pricing agent models
- `AnalyticsDashboard`: Generates performance reports

**Input:**
```json
{
  "rfp_id": "RFP-2025-001",
  "submitted_at": "2025-11-10T14:00:00Z",
  "outcome": "won",
  "actual_price": 4400000.00,
  "predicted_price": 4450000.00,
  "match_accuracy": 0.95
}
```

**Output:**
```json
{
  "retraining_triggered": true,
  "model_version": "v2.1",
  "performance_metrics": {
    "win_rate": 0.68,
    "match_accuracy": 0.91,
    "pricing_accuracy": 0.87
  }
}
```

**Interface:**
```python
class LearningAgent:
    def record_outcome(self, feedback: Feedback) -> None
    def calculate_metrics(self) -> Dict
    def retrain_models(self, min_samples: int = 50) -> bool
    def update_agent_models(self, model_path: str) -> None
```

### 7. Shared Memory Layer

**Responsibility:** Centralized data storage accessible by all agents

**Components:**

**PostgreSQL Schema:**
```sql
-- RFPs table
CREATE TABLE rfps (
    rfp_id VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    deadline TIMESTAMP,
    scope TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Specifications table
CREATE TABLE specifications (
    spec_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id),
    specifications JSONB,
    testing_requirements JSONB,
    confidence_score FLOAT
);

-- Products table
CREATE TABLE products (
    sku VARCHAR(50) PRIMARY KEY,
    product_name TEXT,
    specifications JSONB,
    unit_price DECIMAL(10,2),
    datasheet_url TEXT
);

-- Matches table
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id),
    sku VARCHAR(50) REFERENCES products(sku),
    match_score FLOAT,
    specification_alignment JSONB
);

-- Pricing table
CREATE TABLE pricing (
    pricing_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id),
    sku VARCHAR(50),
    pricing_breakdown JSONB,
    total_estimate DECIMAL(12,2)
);

-- Feedback table
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id),
    outcome VARCHAR(20),
    actual_price DECIMAL(12,2),
    submitted_at TIMESTAMP
);
```

**Redis Cache Structure:**
```python
# Temporary agent communication
redis_keys = {
    "rfp:{rfp_id}:status": "processing",
    "rfp:{rfp_id}:current_agent": "technical",
    "rfp:{rfp_id}:results": "{json_data}",
    "agent:sales:queue": "[rfp_id1, rfp_id2]"
}
```

### 8. Frontend Dashboard

**Responsibility:** Visualize RFP pipeline and provide user interface

**Components:**
- `RFPListView`: Displays all RFPs with status indicators
- `RFPDetailView`: Shows detailed results for a specific RFP
- `AnalyticsView`: Performance metrics and charts
- `AlertSystem`: Deadline notifications

**Design System (Olive Green Theme):**
```css
:root {
  --primary: #556B2F;        /* Dark Olive Green */
  --primary-light: #6B8E23;  /* Olive Drab */
  --primary-dark: #3D4F1F;   /* Deep Olive */
  --accent: #9ACD32;         /* Yellow Green */
  --background: #F5F5DC;     /* Beige */
  --text: #2F4F2F;           /* Dark Slate Gray */
  --success: #228B22;        /* Forest Green */
  --warning: #DAA520;        /* Goldenrod */
  --error: #8B4513;          /* Saddle Brown */
}
```

**Key UI Components:**
- Dashboard with RFP cards showing status, deadline, match score
- Detailed view with specification comparison tables
- Pricing breakdown with line items
- Analytics charts (win rate trends, processing time)
- Alert badges for approaching deadlines

## Data Models

### RFPSummary
```python
@dataclass
class RFPSummary:
    rfp_id: str
    title: str
    source: str
    deadline: datetime
    scope: str
    testing_requirements: List[str]
    discovered_at: datetime
    status: str  # new, processing, completed, submitted
```

### Specification
```python
@dataclass
class Specification:
    rfp_id: str
    specifications: Dict[str, Any]
    testing_requirements: Dict[str, List[str]]
    confidence_score: float
```

### ProductMatch
```python
@dataclass
class ProductMatch:
    sku: str
    product_name: str
    match_score: float
    specification_alignment: Dict[str, str]
    datasheet_url: str
```

### PricingBreakdown
```python
@dataclass
class PricingBreakdown:
    sku: str
    unit_price: float
    quantity: int
    subtotal: float
    testing_cost: float
    delivery_cost: float
    urgency_adjustment: float
    total: float
    currency: str
```

### RFPResponse
```python
@dataclass
class RFPResponse:
    rfp_id: str
    rfp_summary: RFPSummary
    specifications: Specification
    matches: List[ProductMatch]
    pricing: List[PricingBreakdown]
    recommended_sku: str
    total_estimate: float
    generated_at: datetime
```

## Error Handling

### Error Categories

1. **Data Extraction Errors**
   - PDF parsing failures → Flag for manual review
   - Missing specifications → Request clarification
   - Corrupted documents → Log and skip

2. **Agent Execution Errors**
   - Agent timeout → Retry up to 3 times with exponential backoff
   - Agent crash → Log error, notify admin, continue with partial results
   - Invalid output → Validate schema, request re-execution

3. **Database Errors**
   - Connection failures → Retry with circuit breaker pattern
   - Query timeouts → Optimize query or increase timeout
   - Data inconsistency → Transaction rollback and retry

4. **API Errors**
   - Rate limiting → Implement exponential backoff
   - Authentication failures → Refresh tokens automatically
   - Network errors → Retry with timeout

### Error Handling Strategy

```python
class ErrorHandler:
    def handle_agent_error(self, agent: str, error: Exception) -> None:
        """
        1. Log error with context
        2. Determine if retryable
        3. Execute retry logic or escalate
        4. Update RFP status
        5. Notify relevant stakeholders
        """
        
    def handle_data_error(self, rfp_id: str, error: Exception) -> None:
        """
        1. Flag RFP for manual review
        2. Store partial results
        3. Notify user of issue
        """
        
    def handle_system_error(self, error: Exception) -> None:
        """
        1. Log critical error
        2. Trigger alerts
        3. Attempt graceful degradation
        4. Notify admin team
        """
```

### Logging Strategy

```python
import logging

# Structured logging with context
logger.info("RFP processing started", extra={
    "rfp_id": rfp_id,
    "agent": "sales",
    "timestamp": datetime.now()
})

# Error logging with stack traces
logger.error("Agent execution failed", extra={
    "rfp_id": rfp_id,
    "agent": "technical",
    "error": str(error),
    "stack_trace": traceback.format_exc()
})
```

## Testing Strategy

### 1. Unit Testing

**Scope:** Individual agent methods and utility functions

**Tools:** pytest, unittest.mock

**Coverage Target:** 80% minimum

**Example Tests:**
```python
def test_sales_agent_parse_rfp():
    agent = SalesAgent()
    html = "<html>...</html>"
    result = agent.parse_rfp(html)
    assert result.rfp_id is not None
    assert result.deadline > datetime.now()

def test_technical_agent_match_score():
    agent = TechnicalAgent()
    rfp_specs = {"voltage": "11kV", "type": "XLPE"}
    product_specs = {"voltage": "11kV", "type": "XLPE"}
    score = agent.calculate_match_score(rfp_specs, product_specs)
    assert score >= 0.9
```

### 2. Integration Testing

**Scope:** Agent interactions and data flow

**Tools:** pytest, testcontainers (for databases)

**Example Tests:**
```python
def test_orchestrator_workflow():
    # Setup test RFP
    rfp = create_test_rfp()
    
    # Execute workflow
    orchestrator = OrchestratorAgent()
    result = orchestrator.process_rfp(rfp.rfp_id)
    
    # Verify all agents executed
    assert result.specifications is not None
    assert len(result.matches) > 0
    assert result.pricing is not None
```

### 3. End-to-End Testing

**Scope:** Complete workflow from RFP discovery to response generation

**Tools:** pytest, Selenium (for UI testing)

**Test Scenarios:**
- Happy path: RFP discovered → parsed → matched → priced → response generated
- Error scenarios: Missing specs, no matches, pricing failures
- Performance: Process 10 RFPs concurrently

### 4. Performance Testing

**Scope:** System scalability and response times

**Tools:** Locust, Apache JMeter

**Metrics:**
- RFP processing time < 30 minutes (standard complexity)
- API response time < 2 seconds (95th percentile)
- Concurrent RFP handling: 1000 requests

### 5. Validation Testing

**Scope:** Accuracy of matching and pricing

**Tools:** Custom validation scripts with sample data

**Approach:**
- Create 50 sample RFPs with known correct matches
- Run through system and compare results
- Calculate accuracy metrics
- Target: 90% match accuracy, 85% pricing accuracy

## Deployment Architecture

### Containerization

**Docker Compose Structure:**
```yaml
version: '3.8'
services:
  orchestrator:
    build: ./orchestrator
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - qdrant
      
  sales-agent:
    build: ./agents/sales
    
  technical-agent:
    build: ./agents/technical
    
  pricing-agent:
    build: ./agents/pricing
    
  learning-agent:
    build: ./agents/learning
    
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7
    
  qdrant:
    image: qdrant/qdrant:latest
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
```

### Cloud Deployment (AWS Example)

**Services:**
- **ECS/EKS**: Container orchestration for agents
- **RDS PostgreSQL**: Managed database
- **ElastiCache Redis**: Managed cache
- **EC2**: Qdrant vector database
- **S3**: Document storage
- **CloudWatch**: Monitoring and logging
- **API Gateway**: REST API management
- **CloudFront**: Frontend CDN

**Scaling Strategy:**
- Horizontal scaling for agents based on queue depth
- Auto-scaling groups for ECS tasks
- Read replicas for PostgreSQL
- Multi-AZ deployment for high availability

### CI/CD Pipeline

**GitHub Actions Workflow:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run unit tests
        run: pytest tests/unit
      - name: Run integration tests
        run: pytest tests/integration
        
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: docker-compose build
      - name: Push to registry
        run: docker-compose push
        
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AWS
        run: |
          aws ecs update-service --cluster rfp-cluster \
            --service orchestrator --force-new-deployment
```

## Security Considerations

1. **Authentication & Authorization**
   - JWT tokens for API access
   - Role-based access control (RBAC)
   - API key management for external integrations

2. **Data Protection**
   - Encryption at rest (database encryption)
   - Encryption in transit (TLS/SSL)
   - PII data masking in logs

3. **Input Validation**
   - Schema validation for all API inputs
   - Sanitization of scraped data
   - PDF malware scanning

4. **Secrets Management**
   - AWS Secrets Manager or HashiCorp Vault
   - No hardcoded credentials
   - Rotation policies for API keys

## Performance Optimization

1. **Caching Strategy**
   - Redis cache for frequently accessed RFPs
   - Product catalog caching
   - API response caching (5-minute TTL)

2. **Database Optimization**
   - Indexes on rfp_id, sku, deadline
   - Query optimization for complex joins
   - Connection pooling

3. **Async Processing**
   - Celery task queue for long-running operations
   - Parallel agent execution where possible
   - Background model retraining

4. **Vector Search Optimization**
   - HNSW index in Qdrant for fast similarity search
   - Batch embedding generation
   - Quantization for reduced memory footprint

## Monitoring and Observability

**Metrics to Track:**
- RFP processing time (avg, p95, p99)
- Agent success/failure rates
- API response times
- Database query performance
- Match accuracy over time
- Win rate trends

**Alerting Rules:**
- Agent failure rate > 5%
- API response time > 5 seconds
- Database connection pool exhausted
- Deadline approaching (48 hours)
- Model accuracy drop > 10%

**Logging:**
- Structured JSON logs
- Centralized logging (ELK stack or CloudWatch)
- Log retention: 90 days
- PII redaction in logs
