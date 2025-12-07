# 🚀 Quick Start Guide - Developer Setup

**Project:** SmartBid Control Tower  
**Last Updated:** December 7, 2025

---

## 🎯 For Developer A (Backend)

### Prerequisites
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Git

### Initial Setup (First Time Only)

#### 1. Clone and Setup Virtual Environment
```bash
cd f:/eytech
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

pip install --upgrade pip
pip install -r requirements.txt
```

#### 2. Install PostgreSQL
```bash
# Windows: Download from https://www.postgresql.org/download/windows/
# Install and remember the password you set

# Create database
psql -U postgres
CREATE DATABASE smartbid_db;
\q
```

#### 3. Install Redis
```bash
# Windows: Download from https://github.com/microsoftarchive/redis/releases
# Or use Docker:
docker run -d -p 6379:6379 redis:7-alpine
```

#### 4. Configure Environment
```bash
# Copy template
copy .env.template .env

# Edit .env with your values:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/smartbid_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

#### 5. Initialize Database
```bash
# Run schema
psql -U postgres -d smartbid_db -f shared/database/schema.sql

# Or use Python script
python shared/database/init_db.py
```

#### 6. Load Sample Data
```bash
# Create sample products
python -c "
from agents.technical.product_loader import load_sample_products
load_sample_products()
print('Sample products loaded!')
"
```

#### 7. Start Backend Server
```bash
uvicorn orchestrator.api.main:app --reload --port 8000
```

#### 8. Test API
```bash
# Open browser to http://localhost:8000/docs
# You should see Swagger UI with all endpoints
```

### Daily Workflow

#### Morning Routine
```bash
cd f:/eytech
git checkout main
git pull origin main
git checkout backend/your-branch
git merge main
venv\Scripts\activate
uvicorn orchestrator.api.main:app --reload --port 8000
```

#### Before Pushing
```bash
# Run tests
pytest tests/test_agents.py
pytest tests/test_api.py

# Check code quality
flake8 orchestrator/ agents/
black orchestrator/ agents/ --check

# Commit and push
git add .
git commit -m "feat(backend): your changes"
git push origin backend/your-branch
```

### Your First Tasks

#### Day 1: Verify Setup
- [ ] Database connected
- [ ] Redis connected
- [ ] All agents importable
- [ ] FastAPI starts without errors
- [ ] `/health` endpoint works
- [ ] Swagger docs accessible

#### Day 2: Create First Endpoint
```python
# In orchestrator/api/routes/rfp.py
@router.post("/submit")
async def submit_rfp(rfp: RFPCreate, db: Session = Depends(get_db)):
    """Submit new RFP for processing"""
    # Your implementation here
    pass
```

#### Day 3: Test Agent Integration
```python
# In tests/test_agents.py
def test_sales_agent():
    agent = SalesAgent()
    result = agent.discover_rfps_from_url("https://example.com")
    assert result is not None
```

### Troubleshooting

#### psycopg2 won't install?
```bash
# Try binary version
pip install psycopg2-binary

# If still fails, install PostgreSQL dev headers
# Windows: Already included in PostgreSQL installer
# Linux: sudo apt-get install libpq-dev python3-dev
```

#### Redis connection failed?
```bash
# Check if Redis is running
redis-cli ping
# Should return PONG

# Or start Docker container
docker start redis
```

#### Import errors?
```bash
# Make sure you're in project root
cd f:/eytech

# Make sure venv is activated
venv\Scripts\activate

# Reinstall packages
pip install -e .
```

---

## 🎨 For Developer B (Frontend)

### Prerequisites
- Node.js 18+ and npm
- Git
- Modern browser (Chrome/Firefox)

### Initial Setup (First Time Only)

#### 1. Install Node.js
```bash
# Download from https://nodejs.org/
# Verify installation
node --version  # Should show v18.x or higher
npm --version   # Should show v9.x or higher
```

#### 2. Setup Frontend
```bash
cd f:/eytech/frontend
npm install
```

#### 3. Configure API URL
```bash
# Edit frontend/src/services/api.js
# Set USE_MOCK_DATA = true for development without backend
# Set USE_MOCK_DATA = false when backend is ready
```

#### 4. Start Development Server
```bash
npm run dev
```

#### 5. Open Browser
```
http://localhost:5173
```

### Daily Workflow

#### Morning Routine
```bash
cd f:/eytech
git checkout main
git pull origin main
git checkout frontend/your-branch
git merge main
cd frontend
npm run dev
```

#### Before Pushing
```bash
# Run linter
npm run lint

# Check build
npm run build

# Commit and push
cd ..
git add .
git commit -m "feat(frontend): your changes"
git push origin frontend/your-branch
```

### Your First Tasks

#### Day 1: Verify Setup
- [ ] Dev server starts
- [ ] Can navigate to all pages
- [ ] Tailwind CSS working
- [ ] Components render correctly
- [ ] No console errors

#### Day 2: Create First Component
```jsx
// In frontend/src/components/Dashboard/KPICard.jsx
export default function KPICard({ title, value, change, icon }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className="text-2xl font-bold">{value}</p>
          <p className={`text-sm ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {change >= 0 ? '↑' : '↓'} {Math.abs(change)}%
          </p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );
}
```

#### Day 3: Connect to API
```javascript
// In frontend/src/services/api.js
export async function getRFPs(filters = {}) {
  if (USE_MOCK_DATA) {
    return mockRFPs;
  }
  
  const response = await fetch(`${baseURL}/rfp/list?${new URLSearchParams(filters)}`);
  const data = await response.json();
  return data.data.rfps;
}
```

### Troubleshooting

#### npm install fails?
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port 5173 already in use?
```bash
# Kill process using port
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Or change port in vite.config.js
```

#### Tailwind CSS not working?
```bash
# Rebuild
npm run build

# Check tailwind.config.js has correct paths
# Check postcss.config.js exists
```

---

## 🤝 Working Together

### Communication Channels

#### Daily Standup (Post in Team Chat)
**Time:** 10:00 AM  
**Format:**
```
✅ Yesterday: Implemented sales agent API
🚧 Today: Working on technical agent matching
🚨 Blockers: Need clarification on price band formula
```

#### API Changes (Post in #api-contract)
**Backend posts:**
```
🔔 API Update: POST /api/agents/sales/intake-url
Request: { url: string, source_type: string }
Response: { ticket_id: string, status: string }
Breaking Change: No
Docs Updated: Yes
```

**Frontend responds:**
```
✅ Acknowledged - Will integrate today
```

### Code Review Process

#### Creating Pull Request
```bash
# Push your branch
git push origin your-branch

# Create PR on GitHub
# Title: [Backend] Add sales agent API
# or
# Title: [Frontend] Create dashboard components

# Description:
## Changes
- Added sales agent endpoints
- Implemented Go/No-Go scoring

## Testing
- [ ] Unit tests pass
- [ ] Manual testing done
- [ ] Swagger docs updated

## Screenshots (for frontend)
[Add screenshots here]
```

#### Reviewing Pull Request
**What to check:**
- ✅ Code follows style guide
- ✅ Tests included
- ✅ Documentation updated
- ✅ No merge conflicts
- ✅ Builds successfully

**How to approve:**
```
✅ LGTM (Looks Good To Me)
- Code quality: Good
- Tests: Pass
- Documentation: Complete
Approved for merge!
```

### Resolving Conflicts

#### If you get merge conflict:
```bash
# Pull latest main
git checkout main
git pull origin main

# Merge into your branch
git checkout your-branch
git merge main

# Conflicts will be marked in files
# Open file and look for:
<<<<<<< HEAD
your code
=======
their code
>>>>>>> main

# Keep the correct version
# Then:
git add .
git commit -m "chore: resolve merge conflicts"
git push origin your-branch
```

---

## 📋 Checklist Before First Commit

### Backend Developer
- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] Database connected and initialized
- [ ] Redis running
- [ ] FastAPI starts without errors
- [ ] `/health` endpoint returns 200
- [ ] Can see Swagger docs at `/docs`
- [ ] Read `.github/copilot-instructions.md`
- [ ] Read `docs/API_CONTRACT.md`
- [ ] Understand agent responsibilities

### Frontend Developer
- [ ] Node modules installed
- [ ] Dev server runs on port 5173
- [ ] All pages load without errors
- [ ] Tailwind CSS working
- [ ] Can see mock data
- [ ] Read `.github/copilot-instructions.md`
- [ ] Read `docs/API_CONTRACT.md`
- [ ] Understand UI flow

---

## 🆘 Getting Help

### Internal Resources
1. `.github/copilot-instructions.md` - Full architecture
2. `docs/API_CONTRACT.md` - API specifications
3. `IMPLEMENTATION_STATUS.md` - Current progress
4. `WORK_DIVISION.md` - Task division

### External Resources
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Tailwind CSS: https://tailwindcss.com/docs
- PostgreSQL: https://www.postgresql.org/docs/

### Ask Your Partner
- Post in team chat
- Tag with @backend or @frontend
- Be specific about the issue
- Share error messages and logs

---

## ✅ Success Criteria

### Week 1 Goals

**Backend:**
- [ ] All services running (PostgreSQL, Redis, FastAPI)
- [ ] Basic CRUD for RFPs working
- [ ] At least 2 agents fully functional
- [ ] API documentation complete

**Frontend:**
- [ ] All pages navigable
- [ ] Dashboard showing mock data
- [ ] RFP submission form working
- [ ] Components library created

**Together:**
- [ ] API contract agreed upon
- [ ] No merge conflicts
- [ ] Daily standups happening
- [ ] Having fun! 🎉

---

**Remember:** 
- Communicate early and often
- Ask questions when stuck
- Review each other's PRs
- Celebrate small wins!

Good luck! 🚀
