# SmartBid Control Tower - Copilot Instructions

**Project:** Multi-Agent RFP Automation System for Wires & Cables OEM  
**Code Name:** SmartBid Control Tower  
**Last Updated:** December 7, 2025

---

## 🎯 Project Overview

You are helping build **SmartBid Control Tower**: an intelligent, multi-agent RFP response assistant for a wires and cables OEM manufacturer. The system automates RFP discovery, technical analysis, product matching, pricing, and proposal generation.

---

## 🏗️ Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Vector DB:** Qdrant (for semantic product search)
- **Agent Orchestration:** LangGraph / CrewAI
- **Task Queue:** Celery (optional) or Redis Streams
- **ORM:** SQLAlchemy + Alembic migrations

### Frontend
- **Language:** TypeScript
- **Framework:** React 18+
- **UI Library:** shadcn/ui
- **Data Tables:** TanStack Table
- **Styling:** Tailwind CSS
- **State Management:** React Query / TanStack Query
- **Routing:** React Router v6

### DevOps
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana (planned)

---

## 🤖 Agent Architecture

### 1. Sales Agent (Scout)
**Role:** RFP Discovery & Qualification

**Responsibilities:**
- Omnichannel intake (web scraping, email parsing, tender portals)
- Extract: RFP title, deadline, client, project type, specifications
- Apply **90-day filter** (discard RFPs with deadline > 90 days)
- Compute **Go/No-Go Score**: `TimeScore + ValueScore + FitScore`
- Push qualified RFPs to Redis queue
- Create `rfp_tickets` database rows with status="NEW"

**Key Metrics:**
- Days until deadline (urgency)
- Estimated project value
- Client type (government, private, repeat customer)
- Technical fit score

**Endpoints:**
- `POST /agents/sales/intake-url` - Scrape and process URL
- `POST /agents/sales/intake-email` - Parse email attachments
- `GET /agents/sales/tickets` - List discovered RFPs

---

### 2. Main Orchestrator Agent
**Role:** Workflow Coordination

**Responsibilities:**
- Pull qualified tickets from Redis queue
- Route tickets to Technical and Pricing agents
- Consolidate agent outputs
- Generate summary for human review
- Update ticket status through lifecycle

**Workflow:**
```
NEW → ANALYZING → MATCHED → PRICED → REVIEWED → APPROVED
```

**Endpoints:**
- `POST /orchestrator/process-ticket/{ticket_id}` - Start processing
- `GET /orchestrator/status/{ticket_id}` - Check progress
- `POST /orchestrator/approve/{ticket_id}` - Human approval

---

### 3. Technical Agent (Engineer)
**Role:** Specification Analysis & Product Matching

**Responsibilities:**
1. **Extract Scope of Supply** from RFP text
   - Parse into structured items (`rfp_scope_items`)
   - Normalize specs: voltage_kv, cores, area_sqmm, insulation_type, etc.

2. **Find Top-3 OEM SKUs** per scope item
   - Search `oem_skus` database
   - Use Qdrant vector search for semantic matching
   - Compute **SpecMatch%** with equal-weight scoring:
     - Voltage match: 20%
     - Conductor size: 20%
     - Insulation type: 20%
     - Conductor material: 20%
     - Standards compliance: 20%

3. **Select Final SKUs**
   - Store matches in `rfp_oem_matches`
   - Pick best match per item in `rfp_final_selection`

**Endpoints:**
- `POST /agents/technical/extract-scope/{ticket_id}` - Parse specifications
- `POST /agents/technical/match-products/{ticket_id}` - Find SKU matches
- `GET /agents/technical/matches/{ticket_id}` - Get match results

---

### 4. Pricing Agent (Vault)
**Role:** Cost Estimation & Pricing Strategy

**Responsibilities:**
1. **Load Product Prices**
   - From `product_prices` (material costs)
   - From `service_prices` (testing, delivery, etc.)

2. **Historical Analysis**
   - Query `historical_tender_lines` for similar past bids
   - Compute median prices per SKU/segment

3. **Generate Price Bands** (per line item)
   - **Aggressive:** Historical median × 0.95 (5% below market)
   - **Balanced:** Historical median × 1.00 (market rate)
   - **Conservative:** Historical median × 1.10 (10% premium)

4. **Consolidated Pricing Table**
   - Store in `rfp_pricing_lines`
   - Include: SKU, quantity, unit_price, testing_cost, delivery_cost, total

**Endpoints:**
- `POST /agents/pricing/calculate/{ticket_id}` - Generate pricing
- `GET /agents/pricing/breakdown/{ticket_id}` - Detailed cost breakdown
- `POST /agents/pricing/apply-strategy/{ticket_id}` - Apply pricing band

---

### 5. Auditor Agent (Red-Team)
**Role:** Quality Assurance & Risk Detection

**Responsibilities:**
1. **Completeness Checks**
   - Verify all required tests specified
   - Check for missing technical clauses
   - Validate delivery terms

2. **Price Anomaly Detection**
   - Compare prices vs historical medians
   - Flag outliers (> 20% deviation)
   - Check for missing cost components

3. **Compliance Validation**
   - Standards compliance (IEC, IS, BS)
   - Certification requirements
   - Warranty clauses

4. **Mark as Validated**
   - Status: VALIDATED or FLAGGED
   - Generate audit report

**Endpoints:**
- `POST /agents/auditor/validate/{ticket_id}` - Run audit
- `GET /agents/auditor/report/{ticket_id}` - Get audit findings

---

### 6. Learning Agent (Optimizer)
**Role:** Continuous Improvement

**Responsibilities:**
1. **Update Spec Weights**
   - Analyze win/loss patterns from `tender_outcomes`
   - Adjust matching weights per segment
   - Store in `pricing_config_segments`

2. **Margin Band Optimization**
   - Track win rates per pricing strategy
   - Adjust aggressive/balanced/conservative multipliers
   - Update pricing rules

3. **Performance Metrics**
   - Win rate by client type, project type
   - Average match accuracy
   - Pricing competitiveness

**Endpoints:**
- `POST /agents/learning/train` - Update models
- `GET /agents/learning/insights` - Get recommendations
- `POST /agents/learning/feedback/{ticket_id}` - Record outcome

---

### 7. Bid Co-Pilot (RAG Chat)
**Role:** Interactive Assistant

**Responsibilities:**
- RAG (Retrieval-Augmented Generation) over:
  - RFP documents
  - OEM product datasheets
  - Historical pricing data
  - Tender outcomes
- Answer questions like:
  - "What's the recommended SKU for 11kV XLPE cable?"
  - "Show me pricing for similar past tenders"
  - "What tests are required for this RFP?"

**Endpoints:**
- `POST /agents/copilot/chat` - Send message
- `GET /agents/copilot/history/{session_id}` - Chat history

---

## 🗄️ Database Schema

### Core Tables

#### 1. `rfp_tickets`
Main RFP tracking table
```sql
CREATE TABLE rfp_tickets (
    ticket_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rfp_title TEXT NOT NULL,
    source_type VARCHAR(50),           -- 'web', 'email', 'portal'
    source_url TEXT,
    client_name VARCHAR(200),
    client_type VARCHAR(50),           -- 'government', 'private', 'repeat'
    project_type VARCHAR(100),         -- 'transmission', 'distribution', 'industrial'
    due_date TIMESTAMP,
    days_until_due INTEGER,
    go_no_go_score DECIMAL(5,2),
    rfp_raw_text TEXT,
    status VARCHAR(50) DEFAULT 'NEW', -- 'NEW', 'ANALYZING', 'MATCHED', 'PRICED', 'REVIEWED', 'APPROVED', 'REJECTED'
    discovered_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rfp_tickets_status ON rfp_tickets(status);
CREATE INDEX idx_rfp_tickets_due_date ON rfp_tickets(due_date);
CREATE INDEX idx_rfp_tickets_score ON rfp_tickets(go_no_go_score DESC);
```

#### 2. `rfp_scope_items`
Parsed scope of supply
```sql
CREATE TABLE rfp_scope_items (
    item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES rfp_tickets(ticket_id) ON DELETE CASCADE,
    item_number INTEGER,
    description TEXT,
    quantity INTEGER,
    unit VARCHAR(20),                  -- 'meters', 'km', 'pieces'
    
    -- Normalized specifications
    voltage_kv DECIMAL(6,2),
    cores INTEGER,
    area_sqmm DECIMAL(8,2),
    insulation_type VARCHAR(50),       -- 'XLPE', 'PVC', 'EPR'
    conductor_material VARCHAR(50),    -- 'Copper', 'Aluminum'
    armour_type VARCHAR(50),           -- 'SWA', 'AWA', 'Unarmored'
    temp_rating INTEGER,               -- 90, 70, etc.
    standards TEXT[],                  -- ['IEC 60502-2', 'IS 7098']
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_scope_items_ticket ON rfp_scope_items(ticket_id);
```

#### 3. `oem_skus`
Product catalog
```sql
CREATE TABLE oem_skus (
    sku VARCHAR(50) PRIMARY KEY,
    product_name TEXT NOT NULL,
    manufacturer VARCHAR(100),
    category VARCHAR(100),
    
    -- Specifications (normalized)
    voltage_kv DECIMAL(6,2),
    cores INTEGER,
    area_sqmm DECIMAL(8,2),
    insulation_type VARCHAR(50),
    conductor_material VARCHAR(50),
    armour_type VARCHAR(50),
    temp_rating INTEGER,
    standards TEXT[],
    
    -- Pricing
    base_unit_price DECIMAL(10,2),
    currency VARCHAR(10) DEFAULT 'INR',
    
    -- Metadata
    datasheet_url TEXT,
    stock_status VARCHAR(50),
    lead_time_days INTEGER,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_oem_skus_category ON oem_skus(category);
CREATE INDEX idx_oem_skus_voltage ON oem_skus(voltage_kv);
```

#### 4. `rfp_oem_matches`
Product matching results
```sql
CREATE TABLE rfp_oem_matches (
    match_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES rfp_tickets(ticket_id) ON DELETE CASCADE,
    item_id UUID REFERENCES rfp_scope_items(item_id) ON DELETE CASCADE,
    sku VARCHAR(50) REFERENCES oem_skus(sku),
    
    match_rank INTEGER,                -- 1, 2, 3 (Top-3)
    spec_match_pct DECIMAL(5,2),      -- 0.00 to 100.00
    
    -- Match score components
    voltage_match BOOLEAN,
    size_match BOOLEAN,
    insulation_match BOOLEAN,
    conductor_match BOOLEAN,
    standards_match BOOLEAN,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_matches_ticket ON rfp_oem_matches(ticket_id);
CREATE INDEX idx_matches_item ON rfp_oem_matches(item_id);
```

#### 5. `rfp_final_selection`
Selected SKUs per item
```sql
CREATE TABLE rfp_final_selection (
    selection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES rfp_tickets(ticket_id) ON DELETE CASCADE,
    item_id UUID REFERENCES rfp_scope_items(item_id) ON DELETE CASCADE,
    sku VARCHAR(50) REFERENCES oem_skus(sku),
    
    selection_reason TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 6. `product_prices`
Material pricing
```sql
CREATE TABLE product_prices (
    price_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) REFERENCES oem_skus(sku),
    
    unit_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    
    effective_from DATE DEFAULT CURRENT_DATE,
    effective_to DATE,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 7. `service_prices`
Testing, delivery, etc.
```sql
CREATE TABLE service_prices (
    service_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_type VARCHAR(100),         -- 'type_test', 'routine_test', 'delivery', 'installation'
    service_name TEXT,
    
    pricing_method VARCHAR(50),        -- 'percentage', 'fixed', 'per_unit'
    base_rate DECIMAL(10,2),
    multiplier DECIMAL(5,4),
    
    effective_from DATE DEFAULT CURRENT_DATE,
    effective_to DATE,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 8. `historical_tender_lines`
Past bid data
```sql
CREATE TABLE historical_tender_lines (
    line_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tender_ref VARCHAR(100),
    tender_date DATE,
    client_name VARCHAR(200),
    client_type VARCHAR(50),
    project_type VARCHAR(100),
    
    sku VARCHAR(50),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(12,2),
    
    won BOOLEAN,
    competitor_price DECIMAL(12,2),
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_historical_sku ON historical_tender_lines(sku);
CREATE INDEX idx_historical_client ON historical_tender_lines(client_type, project_type);
```

#### 9. `rfp_pricing_lines`
Generated pricing for current RFPs
```sql
CREATE TABLE rfp_pricing_lines (
    pricing_line_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES rfp_tickets(ticket_id) ON DELETE CASCADE,
    item_id UUID REFERENCES rfp_scope_items(item_id) ON DELETE CASCADE,
    sku VARCHAR(50) REFERENCES oem_skus(sku),
    
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    
    -- Cost components
    material_cost DECIMAL(12,2),
    testing_cost DECIMAL(12,2),
    delivery_cost DECIMAL(12,2),
    margin_pct DECIMAL(5,2),
    
    total_price DECIMAL(12,2),
    
    -- Price bands
    aggressive_price DECIMAL(12,2),
    balanced_price DECIMAL(12,2),
    conservative_price DECIMAL(12,2),
    
    selected_strategy VARCHAR(50),     -- 'aggressive', 'balanced', 'conservative'
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 10. `tender_outcomes`
Win/loss tracking
```sql
CREATE TABLE tender_outcomes (
    outcome_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID REFERENCES rfp_tickets(ticket_id),
    
    outcome VARCHAR(50),               -- 'WON', 'LOST', 'WITHDRAWN'
    win_probability DECIMAL(5,2),
    actual_won BOOLEAN,
    
    our_total_price DECIMAL(12,2),
    competitor_price DECIMAL(12,2),
    price_difference_pct DECIMAL(5,2),
    
    feedback_notes TEXT,
    lessons_learned TEXT,
    
    outcome_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 11. `pricing_config_segments`
Learning agent configuration
```sql
CREATE TABLE pricing_config_segments (
    config_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    segment_name VARCHAR(100),         -- 'government_transmission', 'private_distribution'
    
    -- Matching weights
    voltage_weight DECIMAL(3,2) DEFAULT 0.20,
    size_weight DECIMAL(3,2) DEFAULT 0.20,
    insulation_weight DECIMAL(3,2) DEFAULT 0.20,
    conductor_weight DECIMAL(3,2) DEFAULT 0.20,
    standards_weight DECIMAL(3,2) DEFAULT 0.20,
    
    -- Pricing multipliers
    aggressive_multiplier DECIMAL(5,4) DEFAULT 0.95,
    balanced_multiplier DECIMAL(5,4) DEFAULT 1.00,
    conservative_multiplier DECIMAL(5,4) DEFAULT 1.10,
    
    -- Performance
    win_rate DECIMAL(5,2),
    avg_margin DECIMAL(5,2),
    
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 High-Level Workflow

```
1. Sales Agent discovers RFP
   ↓
2. Filter: days_until_due <= 90
   ↓
3. Compute go_no_go_score
   ↓
4. Push to Redis queue → Create rfp_tickets (status=NEW)
   ↓
5. Main Orchestrator pulls ticket (status=ANALYZING)
   ↓
6. Technical Agent:
   - Extract scope → rfp_scope_items
   - Match products → rfp_oem_matches (Top-3 per item)
   - Select final → rfp_final_selection
   ↓
7. Status = MATCHED
   ↓
8. Pricing Agent:
   - Query historical_tender_lines
   - Calculate price bands (aggressive/balanced/conservative)
   - Store in rfp_pricing_lines
   ↓
9. Status = PRICED
   ↓
10. Auditor Agent:
    - Check completeness
    - Validate pricing vs historical
    - Mark as VALIDATED or FLAGGED
    ↓
11. Human review (status = REVIEWED)
    ↓
12. Approval (status = APPROVED) or Rejection
    ↓
13. Learning Agent updates weights from outcomes
```

---

## 🎨 Frontend UI - "SmartBid Cockpit"

### Main Dashboard
- **KPI Cards:**
  - Active RFPs (status != 'APPROVED' | 'REJECTED')
  - Win rate (last 30 days)
  - Avg. processing time
  - Total pipeline value

- **RFP List Table:**
  - Columns: RFP Title, Client, Due Date, Days Left, Status, Go/No-Go Score
  - Filters: Status, Client Type, Date Range
  - Sort: Score, Deadline, Date Created
  - Actions: View Details, Approve, Reject

### Agent-Specific Pages

1. **Sales Agent Dashboard** (`/agents/sales`)
   - Recent discoveries
   - Qualification metrics
   - Source breakdown (web, email, portal)

2. **Technical Matches** (`/agents/technical`)
   - Scope items table
   - Top-3 matches per item with SpecMatch%
   - SKU selection interface

3. **Pricing Workbench** (`/agents/pricing`)
   - Line item pricing table
   - Price band toggle (aggressive/balanced/conservative)
   - Historical comparison charts

4. **Audit Reports** (`/agents/auditor`)
   - Validation checklist
   - Flagged issues
   - Compliance status

5. **Learning Insights** (`/agents/learning`)
   - Win/loss analysis
   - Spec weight adjustments
   - Pricing strategy performance

### Bid Co-Pilot (RAG Chat)
- **Right sidebar** or **modal dialog**
- Chat interface with context-aware responses
- Quick actions: "Show similar tenders", "Explain pricing", "Find SKU alternatives"

---

## 📐 Development Guidelines

### Code Organization
```
smartbid/
├── backend/
│   ├── agents/
│   │   ├── sales.py
│   │   ├── orchestrator.py
│   │   ├── technical.py
│   │   ├── pricing.py
│   │   ├── auditor.py
│   │   ├── learning.py
│   │   └── copilot.py
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── rfp.py
│   │       ├── sales.py
│   │       ├── technical.py
│   │       ├── pricing.py
│   │       └── auditor.py
│   ├── models/
│   │   └── database.py
│   ├── services/
│   │   ├── redis_queue.py
│   │   ├── qdrant_search.py
│   │   └── llm_service.py
│   └── alembic/
│       └── versions/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
└── .github/
    └── copilot-instructions.md (this file)
```

### Coding Standards
- **Type hints:** Always use Python type hints
- **Docstrings:** Use Google-style docstrings
- **Error handling:** Try-except with specific exceptions
- **Logging:** Use Python logging module, not print()
- **Async:** Use async/await for I/O operations
- **Tests:** Write unit tests for all agent logic

### API Response Format
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed",
  "timestamp": "2025-12-07T10:30:00Z"
}
```

### Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Missing required field: client_name",
    "details": { ... }
  },
  "timestamp": "2025-12-07T10:30:00Z"
}
```

---

## 🚀 Implementation Phases

### Phase 1: Backend Skeleton (Week 1)
- [x] FastAPI setup
- [ ] SQLAlchemy models
- [ ] Alembic migrations
- [ ] Redis connection
- [ ] Health check endpoint
- [ ] Basic CRUD for rfp_tickets

### Phase 2: Sales Agent (Week 2)
- [ ] Web scraping logic
- [ ] 90-day filter
- [ ] Go/No-Go scoring
- [ ] Redis queue integration
- [ ] API endpoints

### Phase 3: Technical Agent (Week 3)
- [ ] Scope extraction (regex + LLM)
- [ ] Spec normalization
- [ ] Qdrant integration
- [ ] Top-3 matching algorithm
- [ ] SKU selection logic

### Phase 4: Pricing Agent (Week 4)
- [ ] Historical data queries
- [ ] Price band calculation
- [ ] Cost component breakdown
- [ ] Pricing strategy selection

### Phase 5: Auditor + Learning (Week 5)
- [ ] Completeness checks
- [ ] Price anomaly detection
- [ ] Spec weight updates
- [ ] Margin optimization

### Phase 6: Frontend UI (Week 6-7)
- [ ] Dashboard
- [ ] RFP table with filters
- [ ] Agent-specific pages
- [ ] Bid Co-Pilot chat

### Phase 7: Integration + Testing (Week 8)
- [ ] End-to-end workflow testing
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation

---

## 💡 Key Principles

1. **Modularity:** Each agent is independent and reusable
2. **Traceability:** Every decision is logged and explainable
3. **Human-in-the-Loop:** Critical decisions require approval
4. **Continuous Learning:** System improves from outcomes
5. **Transparency:** All scores and prices show reasoning

---

## 🔐 Security & Compliance

- [ ] API authentication (JWT tokens)
- [ ] Role-based access control (RBAC)
- [ ] Audit logs for all actions
- [ ] Data encryption at rest and in transit
- [ ] GDPR compliance for client data
- [ ] Rate limiting on public endpoints

---

## 📝 Notes for Copilot

- **Always read this file first** before making changes
- **Follow the database schema exactly** - do not rename columns
- **Use the specified tech stack** - no substitutions
- **Agent boundaries are strict** - don't mix responsibilities
- **Test coverage is mandatory** - minimum 80%
- **Document all TODOs** - for external integrations
- **Respect the workflow sequence** - agents run in order

---

**Version:** 1.0  
**Maintained by:** SmartBid Development Team
