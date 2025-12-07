# 🤝 SmartBid Work Division - 2 Developers

**Last Updated:** December 7, 2025  
**Strategy:** Module-based separation to minimize merge conflicts

---

## 🎯 Division Strategy

### Core Principles
1. **Developer A (Backend)** - Focuses on database, APIs, and backend agents
2. **Developer B (Frontend)** - Focuses on UI, user experience, and frontend logic
3. **Shared Files** - Minimal overlap, well-documented when necessary
4. **Communication Points** - API contracts, data models, environment setup

---

## 👨‍💻 Developer A - Backend Engineer

### Primary Responsibility
**Backend Infrastructure, Database, AI Agents, APIs**

### Your Directories (Full Ownership)
```
eytech/
├── orchestrator/           ← YOU OWN THIS
│   ├── __init__.py
│   ├── config.py
│   ├── workflow.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py        ← FastAPI entry point
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── analytics.py
│   │       ├── products.py
│   │       ├── rfp.py
│   │       └── auditor.py  ← NEW (you'll create)
│   │       └── learning.py ← NEW (you'll create)
│   └── services/
│       ├── __init__.py
│       ├── analytics_service.py
│       ├── product_service.py
│       ├── rfp_service.py
│       └── orchestrator_service.py ← NEW (you'll create)
│
├── agents/                 ← YOU OWN THIS
│   ├── __init__.py
│   ├── sales/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── document/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── technical/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── product_loader.py
│   ├── pricing/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── learning/
│   │   ├── __init__.py
│   │   └── agent.py
│   └── auditor/           ← NEW (you'll create)
│       ├── __init__.py
│       └── agent.py
│
├── shared/                 ← YOU OWN THIS
│   ├── models.py          ← Database models
│   ├── database/
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   └── schema.sql
│   └── cache/
│       └── redis_manager.py
│
├── tests/                  ← YOU OWN THIS
│   ├── test_agents.py     ← NEW (you'll create)
│   ├── test_api.py        ← NEW (you'll create)
│   └── verify_backend.py
│
├── docker/                 ← YOU OWN THIS
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── postgres/
│
└── data/                   ← YOU OWN THIS
    ├── products.json      ← Product catalog
    └── sample_rfps/       ← Test data
```

### Your Tasks (Backend Implementation)

#### Phase 1: Database & Core Infrastructure (Days 1-2)
- [ ] **Set up PostgreSQL**
  - Install PostgreSQL locally
  - Create database `smartbid_db`
  - Run `shared/database/schema.sql` to create all 11 tables
  - Load sample data into `oem_skus`, `product_prices`, `historical_tender_lines`

- [ ] **Fix Python Dependencies**
  - Resolve `psycopg2-binary` installation
  - Install PostgreSQL dev headers if needed
  - Find alternative for `crewai==0.1.26` or install from source
  - Update `requirements.txt` with working versions

- [ ] **Configure Environment**
  - Set up `.env` with database credentials
  - Configure Redis connection
  - Test database connection with `shared/database/connection.py`

#### Phase 2: API Layer (Days 3-4)
- [ ] **Complete Main Orchestrator API**
  - `POST /api/orchestrator/process-ticket/{ticket_id}` - Start processing
  - `GET /api/orchestrator/status/{ticket_id}` - Check progress
  - `POST /api/orchestrator/approve/{ticket_id}` - Human approval

- [ ] **Sales Agent API Routes**
  - `POST /api/agents/sales/intake-url` - Scrape and process URL
  - `POST /api/agents/sales/intake-email` - Parse email attachments
  - `GET /api/agents/sales/tickets` - List discovered RFPs

- [ ] **Technical Agent API Routes**
  - `POST /api/agents/technical/extract-scope/{ticket_id}` - Parse specifications
  - `POST /api/agents/technical/match-products/{ticket_id}` - Find SKU matches
  - `GET /api/agents/technical/matches/{ticket_id}` - Get match results

- [ ] **Pricing Agent API Routes**
  - `POST /api/agents/pricing/calculate/{ticket_id}` - Generate pricing
  - `GET /api/agents/pricing/breakdown/{ticket_id}` - Detailed cost breakdown
  - `POST /api/agents/pricing/apply-strategy/{ticket_id}` - Apply pricing band

- [ ] **Auditor Agent (NEW)**
  - Create `agents/auditor/agent.py`
  - Implement completeness checks
  - Implement price anomaly detection
  - Create API routes: `POST /api/agents/auditor/validate/{ticket_id}`

- [ ] **Learning Agent API Routes (NEW)**
  - Create `orchestrator/api/routes/learning.py`
  - `POST /api/agents/learning/train` - Update models
  - `GET /api/agents/learning/insights` - Get recommendations
  - `POST /api/agents/learning/feedback/{ticket_id}` - Record outcome

#### Phase 3: Agent Logic Enhancement (Days 5-6)
- [ ] **Sales Agent**
  - Implement 90-day filter logic
  - Compute Go/No-Go score formula
  - Push to Redis queue
  - Create `rfp_tickets` rows with status="NEW"

- [ ] **Technical Agent**
  - Enhance spec extraction with LLM
  - Implement equal-weight scoring (20% each for 5 criteria)
  - Store matches in `rfp_oem_matches` table
  - Select final SKUs in `rfp_final_selection`

- [ ] **Pricing Agent**
  - Query `historical_tender_lines` for past bids
  - Calculate price bands (0.95/1.00/1.10 multipliers)
  - Store in `rfp_pricing_lines` table
  - Implement cost breakdown (material + testing + delivery)

- [ ] **Auditor Agent**
  - Completeness validation
  - Price anomaly detection (> 20% deviation)
  - Standards compliance checks
  - Generate audit reports

- [ ] **Learning Agent**
  - Implement weight update logic
  - Win/loss analysis from `tender_outcomes`
  - Update `pricing_config_segments`

#### Phase 4: Integration & Testing (Days 7-8)
- [ ] **End-to-End Workflow**
  - Test complete pipeline: URL → Processing → Pricing → Approval
  - Verify all database insertions
  - Test Redis queue operations

- [ ] **Write Backend Tests**
  - Unit tests for each agent
  - Integration tests for API endpoints
  - Database transaction tests

- [ ] **API Documentation**
  - Update Swagger/OpenAPI docs
  - Add example requests/responses
  - Document error codes

### Your Files to Modify
- ✅ `orchestrator/api/main.py` - Add new routes
- ✅ `orchestrator/api/routes/*.py` - Implement endpoints
- ✅ `orchestrator/services/*.py` - Business logic
- ✅ `orchestrator/workflow.py` - Orchestration flow
- ✅ `agents/*/agent.py` - Agent implementations
- ✅ `shared/models.py` - Database models
- ✅ `shared/database/schema.sql` - Database schema
- ✅ `requirements.txt` - Python dependencies
- ✅ `docker/docker-compose.yml` - Container setup
- ✅ `.env` - Environment config

### Your Communication Points with Dev B
1. **API Contract**: Document all endpoint signatures in `docs/API_CONTRACT.md`
2. **Response Formats**: Stick to standard format from `.github/copilot-instructions.md`
3. **Data Models**: Share any changes to response structures
4. **Environment Variables**: Update `.env.template` when adding new configs

---

## 👩‍💻 Developer B - Frontend Engineer

### Primary Responsibility
**User Interface, User Experience, Frontend State Management**

### Your Directories (Full Ownership)
```
eytech/
├── frontend/               ← YOU OWN THIS
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── README.md
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── Layout/
│       │   │   ├── Layout.jsx
│       │   │   ├── Header.jsx
│       │   │   └── Sidebar.jsx
│       │   ├── Dashboard/      ← NEW (you'll create)
│       │   │   ├── KPICard.jsx
│       │   │   ├── MetricsChart.jsx
│       │   │   └── ActivityFeed.jsx
│       │   ├── RFP/            ← NEW (you'll create)
│       │   │   ├── RFPTable.jsx
│       │   │   ├── RFPFilters.jsx
│       │   │   ├── RFPCard.jsx
│       │   │   └── StatusBadge.jsx
│       │   ├── Agents/         ← NEW (you'll create)
│       │   │   ├── SalesAgent.jsx
│       │   │   ├── TechnicalAgent.jsx
│       │   │   ├── PricingAgent.jsx
│       │   │   ├── AuditorAgent.jsx
│       │   │   └── LearningAgent.jsx
│       │   └── Copilot/        ← NEW (you'll create)
│       │       ├── ChatInterface.jsx
│       │       ├── MessageBubble.jsx
│       │       └── QuickActions.jsx
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── RFPList.jsx
│       │   ├── RFPDetail.jsx
│       │   ├── SubmitRFP.jsx
│       │   ├── Products.jsx
│       │   ├── Analytics.jsx
│       │   └── Agents/         ← NEW (you'll create)
│       │       ├── SalesDashboard.jsx
│       │       ├── TechnicalMatches.jsx
│       │       ├── PricingWorkbench.jsx
│       │       ├── AuditReports.jsx
│       │       └── LearningInsights.jsx
│       ├── services/
│       │   ├── api.js         ← API client
│       │   └── mockData.js    ← Mock data (for dev)
│       ├── utils/
│       │   ├── specExtractor.js
│       │   ├── productMatcher.js
│       │   ├── pricingCalculator.js
│       │   └── formatters.js  ← NEW (you'll create)
│       ├── hooks/              ← NEW (you'll create)
│       │   ├── useRFPs.js
│       │   ├── useAgents.js
│       │   └── useCopilot.js
│       └── tests/
│           ├── README.md
│           └── test-rfp-processing.html
│
└── docs/                   ← YOU OWN SOME OF THIS
    ├── USER_GUIDE.md      ← NEW (you'll create)
    └── UI_COMPONENTS.md   ← NEW (you'll create)
```

### Your Tasks (Frontend Implementation)

#### Phase 1: UI Component Library (Days 1-2)
- [ ] **Create Reusable Components**
  - `components/Dashboard/KPICard.jsx` - Metric display cards
  - `components/Dashboard/MetricsChart.jsx` - Charts with Recharts
  - `components/Dashboard/ActivityFeed.jsx` - Recent activity list
  - `components/RFP/RFPTable.jsx` - TanStack Table with filters
  - `components/RFP/RFPFilters.jsx` - Status, date, client filters
  - `components/RFP/StatusBadge.jsx` - Color-coded status badges

- [ ] **Enhance Layout**
  - Add breadcrumbs to `components/Layout/Header.jsx`
  - Add agent quick-links to `components/Layout/Sidebar.jsx`
  - Add notifications dropdown
  - Add user profile menu

#### Phase 2: Agent-Specific Pages (Days 3-4)
- [ ] **Sales Agent Dashboard** (`pages/Agents/SalesDashboard.jsx`)
  - Recent discoveries table
  - Qualification metrics (pie chart)
  - Source breakdown (bar chart)
  - Quick actions: "Scrape URL", "Process Email"

- [ ] **Technical Matches Page** (`pages/Agents/TechnicalMatches.jsx`)
  - Scope items table with expandable rows
  - Top-3 matches per item with SpecMatch%
  - SKU selection interface (radio buttons)
  - Match confidence visualization

- [ ] **Pricing Workbench** (`pages/Agents/PricingWorkbench.jsx`)
  - Line item pricing table (editable)
  - Price band toggle (aggressive/balanced/conservative)
  - Historical comparison chart
  - Cost breakdown accordion

- [ ] **Audit Reports** (`pages/Agents/AuditReports.jsx`)
  - Validation checklist with checkboxes
  - Flagged issues list (red/yellow/green)
  - Compliance status cards
  - Export report button

- [ ] **Learning Insights** (`pages/Agents/LearningInsights.jsx`)
  - Win/loss analysis charts
  - Spec weight adjustments (sliders)
  - Pricing strategy performance (line chart)
  - Recommendations list

#### Phase 3: Bid Co-Pilot (RAG Chat) (Days 5-6)
- [ ] **Chat Interface** (`components/Copilot/ChatInterface.jsx`)
  - Chat window (right sidebar or modal)
  - Message input with send button
  - Message history with scrolling
  - Typing indicator
  - Context-aware suggestions

- [ ] **Quick Actions** (`components/Copilot/QuickActions.jsx`)
  - "Show similar tenders"
  - "Explain pricing"
  - "Find SKU alternatives"
  - "Check compliance"

- [ ] **Message Components** (`components/Copilot/MessageBubble.jsx`)
  - User messages (right-aligned, blue)
  - Bot messages (left-aligned, gray)
  - Code blocks with syntax highlighting
  - Tables in responses
  - Loading skeleton

#### Phase 4: Enhanced Dashboard (Days 7-8)
- [ ] **Main Dashboard Enhancements**
  - Real-time KPI updates
  - Interactive charts (click to drill down)
  - RFP pipeline visualization (Kanban/funnel)
  - Urgent RFPs widget (< 7 days)

- [ ] **Analytics Page Enhancements**
  - Date range picker
  - Export to CSV/PDF
  - Comparison mode (this month vs last month)
  - Custom metric builder

- [ ] **Products Page Enhancements**
  - Product catalog with filters
  - SKU search with autocomplete
  - Product comparison tool
  - Datasheet preview

#### Phase 5: Backend Integration (Days 9-10)
- [ ] **Switch from Mock to Real API**
  - Change `USE_MOCK_DATA = false` in `services/api.js`
  - Update `baseURL` to `http://localhost:8000/api`
  - Add error handling for API failures
  - Add retry logic for failed requests

- [ ] **State Management**
  - Create custom hooks in `hooks/`
  - `useRFPs()` - Fetch and cache RFP data
  - `useAgents()` - Agent status and actions
  - `useCopilot()` - Chat state management

- [ ] **Real-time Updates**
  - Add WebSocket connection for live updates
  - Show notifications for status changes
  - Auto-refresh dashboard metrics

### Your Files to Modify
- ✅ `frontend/src/pages/*.jsx` - All page components
- ✅ `frontend/src/components/**/*.jsx` - All UI components
- ✅ `frontend/src/services/api.js` - API client config
- ✅ `frontend/src/utils/*.js` - Utility functions
- ✅ `frontend/src/hooks/*.js` - Custom React hooks
- ✅ `frontend/package.json` - NPM dependencies
- ✅ `frontend/tailwind.config.js` - Styling config
- ✅ `frontend/vite.config.js` - Build config

### Your Communication Points with Dev A
1. **API Contract**: Read `docs/API_CONTRACT.md` for endpoint specs
2. **Response Formats**: Expect standard format from backend
3. **Data Models**: Ask for TypeScript interfaces for API responses
4. **Testing**: Test with mock data first, then real backend

---

## 🤝 Shared Files (Coordinate Changes)

### Files That Need Coordination

#### 1. `.github/copilot-instructions.md`
- **Who**: Both developers can read, Backend owner for updates
- **Why**: Single source of truth for architecture
- **Rule**: Backend dev updates, Frontend dev reviews

#### 2. `docs/API_CONTRACT.md` (NEW - Backend creates)
- **Who**: Backend creates, Frontend consumes
- **Why**: Endpoint specifications
- **Rule**: Backend updates before implementing, Frontend uses as reference

#### 3. `.env` and `.env.template`
- **Who**: Backend creates, Frontend adds frontend-specific vars
- **Why**: Environment configuration
- **Rule**: Backend handles `DATABASE_URL`, `REDIS_URL`, Frontend handles `VITE_API_URL`

#### 4. `README.md`
- **Who**: Both contribute
- **Why**: Project documentation
- **Rule**: Backend adds setup instructions, Frontend adds UI screenshots

#### 5. `docker/docker-compose.yml`
- **Who**: Backend owns, Frontend reviews
- **Why**: Container orchestration
- **Rule**: Backend manages services, Frontend adds frontend service if needed

---

## 📋 Git Workflow to Avoid Conflicts

### Branch Strategy

#### Developer A (Backend)
```bash
# Create backend branch
git checkout -b backend/phase-1-database
git checkout -b backend/phase-2-apis
git checkout -b backend/phase-3-agents
git checkout -b backend/phase-4-integration
```

#### Developer B (Frontend)
```bash
# Create frontend branch
git checkout -b frontend/phase-1-components
git checkout -b frontend/phase-2-agent-pages
git checkout -b frontend/phase-3-copilot
git checkout -b frontend/phase-4-dashboard
```

### Daily Workflow

#### Morning Sync
```bash
# Both devs do this every morning
git checkout main
git pull origin main

# Backend dev
git checkout backend/current-branch
git merge main  # Merge any changes from main

# Frontend dev
git checkout frontend/current-branch
git merge main  # Merge any changes from main
```

#### Before Pushing
```bash
# Make sure your changes are committed
git add .
git commit -m "feat: describe your changes"

# Pull latest from main
git checkout main
git pull origin main

# Merge main into your branch
git checkout your-branch
git merge main

# Resolve conflicts if any
# Then push
git push origin your-branch
```

### Pull Request Strategy

#### Backend PRs
- **Title**: `[Backend] Phase 1: Database Setup`
- **Reviewers**: Frontend dev (for API contracts)
- **Merge Order**: Backend features first, then frontend consumes

#### Frontend PRs
- **Title**: `[Frontend] Phase 1: UI Components`
- **Reviewers**: Backend dev (for data model understanding)
- **Merge Order**: After backend APIs are merged

### Conflict Resolution Rules

1. **If conflict in `.github/copilot-instructions.md`**: Backend wins
2. **If conflict in `requirements.txt`**: Backend wins
3. **If conflict in `package.json`**: Frontend wins
4. **If conflict in `.env.template`**: Both add their vars, merge manually
5. **If conflict in `README.md`**: Merge manually, combine both sections

---

## 📞 Communication Protocol

### Daily Standup (Async)
**Both devs post in team chat at 10 AM:**
- ✅ What I completed yesterday
- 🚧 What I'm working on today
- 🚨 Any blockers or conflicts

### API Contract Updates
**Backend dev posts when creating/updating endpoints:**
```
🔔 API Update: Added POST /api/agents/sales/intake-url
Request: { url: string, source_type: string }
Response: { ticket_id: string, status: string }
Docs: See docs/API_CONTRACT.md
```

### Frontend Feedback
**Frontend dev posts when needing backend changes:**
```
💬 Need: Dashboard endpoint should include last_updated timestamp
Reason: For showing "Last updated 5 mins ago"
Urgency: Medium (nice-to-have)
```

---

## 🎯 First Week Milestone Goals

### By End of Week 1

#### Developer A (Backend) Checklist
- [ ] PostgreSQL running with all 11 tables
- [ ] FastAPI server starts without errors
- [ ] All 5 agents tested independently
- [ ] Basic CRUD endpoints working for RFPs
- [ ] Sample data loaded (10 products, 5 historical tenders)
- [ ] `docs/API_CONTRACT.md` created with all endpoints

#### Developer B (Frontend) Checklist
- [ ] All reusable components created (KPICard, RFPTable, etc.)
- [ ] Dashboard shows mock data beautifully
- [ ] RFP submission works with mock backend
- [ ] All pages navigable with React Router
- [ ] Responsive design tested (mobile/tablet/desktop)
- [ ] Ready to consume real API (just flip USE_MOCK_DATA flag)

---

## 🚀 Success Metrics

### Independence Score: **95%**
- Only 5% of work overlaps (shared docs, env vars)
- Each dev owns their domain completely
- Minimal merge conflicts expected

### Completion Targets
- **Week 1**: 40% progress (setup + foundations)
- **Week 2**: 75% progress (agents + UI pages)
- **Week 3**: 95% progress (integration + polish)
- **Week 4**: 100% (testing + deployment)

---

## 📝 Quick Reference

### Developer A Commands
```bash
# Start backend
cd f:/eytech
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn orchestrator.api.main:app --reload --port 8000

# Test database
python shared/database/init_db.py

# Run agent tests
pytest tests/test_agents.py
```

### Developer B Commands
```bash
# Start frontend
cd f:/eytech/frontend
npm install
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

---

**Remember:** Communication is key! Post updates, ask questions, and review each other's PRs. You got this! 🚀
