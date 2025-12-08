# 🚀 Complete Setup Guide - RFP Automation System

**Last Updated:** December 8, 2025

---

## 📋 Prerequisites

Before starting, ensure you have:

### Required Software
- ✅ **Python 3.10+** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Download](https://nodejs.org/)
- ✅ **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/windows/)
- ⚠️ **Redis** (Optional for now) - [Download](https://github.com/microsoftarchive/redis/releases)

### Optional (for full features)
- 🔑 **Google API Key** (for Gemini Chatbot) - [Get Key](https://makersuite.google.com/app/apikey)
- 📧 **Email Credentials** (for IMAP monitoring) - Gmail/Outlook

---

## 🎯 Quick Start (3 Options)

### Option 1: Frontend Only (No Setup Required) ⚡
**Best for:** Quick demo, testing UI

```bash
cd f:\eytech\frontend
npm install
npm run dev
```

✅ **Works immediately!** Visit http://localhost:5173

**Features Available:**
- Submit RFP with text
- Extract specifications
- Match products
- Calculate pricing
- View all pages

---

### Option 2: Full Stack with Database 🚀
**Best for:** Complete system, production-ready

Follow the steps below ⬇️

---

### Option 3: Backend Only (API Testing) 🔧
**Best for:** Testing agents, API development

```bash
cd f:\eytech
pip install fastapi uvicorn google-generativeai
uvicorn orchestrator.api.main:app --reload --port 8000
```

Visit http://localhost:8000/docs for API documentation

---

## 📦 Step-by-Step Full Stack Setup

### Step 1: Install PostgreSQL

#### Windows Installation
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run installer
3. **Important:** Remember the password you set for `postgres` user
4. Default port: `5432` (keep it)
5. Install pgAdmin (optional, for GUI management)

#### Verify Installation
```bash
psql --version
# Should show: psql (PostgreSQL) 15.x
```

---

### Step 2: Configure Environment

1. **Copy template:**
```bash
cd f:\eytech
copy .env.template .env
```

2. **Edit `.env` file** with your credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rfp_automation
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD_HERE  # ← Change this!

# Redis Configuration (Optional for now)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Google Gemini (Optional - for chatbot)
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE  # ← Add if you have one

# Email Configuration (Optional - for monitoring)
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here  # ← Use app password, not regular password

# Application Settings
MAX_WORKERS=4
LOG_LEVEL=INFO
```

---

### Step 3: Install Python Dependencies

```bash
cd f:\eytech

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** If `psycopg2-binary` fails:
```bash
# Install PostgreSQL development headers first
# Or use: pip install psycopg2-binary --no-binary psycopg2-binary
```

---

### Step 4: Initialize Database

```bash
# Make sure PostgreSQL is running
# Make sure you're in the project root (f:\eytech)

# Run database initialization
python shared/database/init_db.py
```

**Expected Output:**
```
============================================================
🚀 Starting Database Initialization
============================================================

📡 Step 1: Verifying PostgreSQL connection...
✅ PostgreSQL server is accessible

🗄️  Step 2: Creating database...
✅ Database 'rfp_automation' created successfully

📊 Step 3: Creating tables...
✅ All tables created successfully
📊 Created 7 tables:
   - feedback
   - model_versions
   - performance_metrics
   - pricing_breakdown
   - product_matches
   - products
   - rfps

✅ Step 4: Verifying setup...
✅ Connected to PostgreSQL: PostgreSQL 15.x...

============================================================
🎉 Database initialization completed successfully!
============================================================
```

---

### Step 5: Seed Sample Data

```bash
# Load sample products and RFPs
python shared/database/seed_data.py
```

**Expected Output:**
```
============================================================
🌱 Starting Data Seeding
============================================================

📡 Connecting to database...
✅ Connected successfully
📦 Seeding products...
✅ Inserted 6 products
📄 Seeding sample RFPs...
✅ Inserted 3 sample RFPs
📊 Seeding performance metrics...
✅ Inserted 3 performance metrics

📊 Verifying seeded data...
   Products: 6
   RFPs: 3
   Metrics: 3

============================================================
🎉 Data seeding completed successfully!
============================================================
```

---

### Step 6: Start Backend Server

```bash
# Make sure you're in project root with venv activated
uvicorn orchestrator.api.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['f:\\eytech']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test it:** Visit http://localhost:8000/docs

You should see Swagger API documentation with all endpoints!

---

### Step 7: Install Frontend Dependencies

**Open a NEW terminal** (keep backend running)

```bash
cd f:\eytech\frontend
npm install
```

---

### Step 8: Start Frontend

```bash
# In the frontend directory
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Visit:** http://localhost:5173

---

### Step 9: Connect Frontend to Backend

1. **Edit** `f:\eytech\frontend\src\services\api.js`

2. **Find this line:**
```javascript
const USE_MOCK_DATA = true;
```

3. **Change to:**
```javascript
const USE_MOCK_DATA = false;
```

4. **Save** and refresh browser

✅ **Now your frontend is connected to the real backend!**

---

## ✅ Verification Checklist

### Database
- [ ] PostgreSQL installed and running
- [ ] Database `rfp_automation` created
- [ ] 7 tables created
- [ ] Sample data loaded (6 products, 3 RFPs)

### Backend
- [ ] Python dependencies installed
- [ ] Backend starts without errors
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Health check passes: http://localhost:8000/health

### Frontend
- [ ] Node dependencies installed
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:5173
- [ ] Can submit RFP and see results

### Integration
- [ ] Frontend connected to backend (`USE_MOCK_DATA = false`)
- [ ] Can create RFP from frontend
- [ ] Data persists in database
- [ ] Can view RFPs from database

---

## 🧪 Testing the System

### Test 1: Submit RFP via Frontend

1. Go to http://localhost:5173
2. Click "Submit RFP" in sidebar
3. Fill in the form:
   - **Title:** Test RFP for 11kV Cables
   - **Description:** Supply of 11kV XLPE copper cables, 185 sq.mm, 3 core, 1000 meters
   - **Deadline:** (pick a future date)
4. Click "Submit"
5. Watch the processing animation
6. See extracted specs, matched products, and pricing

### Test 2: Verify Database

```bash
# Connect to database
psql -U postgres -d rfp_automation

# Check RFPs
SELECT rfp_id, title, status FROM rfps;

# Check products
SELECT sku, product_name, unit_price FROM products;

# Exit
\q
```

### Test 3: Test Chatbot

1. Click the chat icon (bottom right)
2. Ask: "What RFPs are currently active?"
3. Should get response from Gemini AI

**Note:** Requires `GOOGLE_API_KEY` in `.env`

### Test 4: Test Email Monitoring

**Note:** Requires email credentials in `.env`

The backend automatically checks email every hour. Check logs:
```
INFO: Starting hourly email check...
INFO: Found X new RFPs from email.
```

---

## 🐛 Troubleshooting

### Problem: Database connection fails

**Error:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   # Windows: Check Services
   services.msc
   # Look for "postgresql-x64-15"
   ```

2. Verify credentials in `.env`
3. Check PostgreSQL is listening on port 5432

---

### Problem: `psycopg2-binary` installation fails

**Error:** `pg_config executable not found`

**Solutions:**
1. Install PostgreSQL development headers
2. Or use pre-built wheel:
   ```bash
   pip install psycopg2-binary --only-binary psycopg2-binary
   ```

---

### Problem: Frontend shows "Network Error"

**Solutions:**
1. Check backend is running on port 8000
2. Check `USE_MOCK_DATA` setting
3. Check CORS settings in backend
4. Open browser console (F12) for detailed errors

---

### Problem: Chatbot doesn't work

**Error:** "Missing API Key"

**Solutions:**
1. Get Google API key: https://makersuite.google.com/app/apikey
2. Add to `.env`: `GOOGLE_API_KEY=your_key_here`
3. Restart backend

---

### Problem: Email monitoring doesn't work

**Solutions:**
1. Use **App Password**, not regular password (for Gmail)
2. Enable IMAP in email settings
3. Check credentials in `.env`
4. Check backend logs for errors

---

## 📊 What's Available Now

### ✅ Fully Working Features

1. **RFP Submission**
   - Via frontend form
   - Via API endpoint
   - Automatic spec extraction
   - Product matching
   - Pricing calculation

2. **Product Catalog**
   - 6 sample products loaded
   - Search and filter
   - View specifications

3. **Analytics Dashboard**
   - KPI cards
   - Charts and graphs
   - Performance metrics

4. **AI Chatbot**
   - Google Gemini 2.5 Flash
   - Context-aware responses
   - Chat history

5. **Email Monitoring**
   - Automatic IMAP checking
   - RFP discovery from inbox
   - Background task (hourly)

6. **Auditor Agent** (NEW!)
   - RFP validation
   - Match quality checking
   - Pricing anomaly detection
   - Compliance reports

### ⚠️ Partially Working

1. **Vector Search**
   - Qdrant not configured
   - Using keyword matching for now

2. **Redis Caching**
   - Optional, system works without it
   - Can install later for performance

---

## 🚀 Next Steps

### Immediate (Today)
1. ✅ Set up database
2. ✅ Load sample data
3. ✅ Test end-to-end flow
4. ✅ Verify all features work

### Short-term (This Week)
1. Add more products to catalog
2. Test with real RFP documents
3. Configure email monitoring
4. Set up Google API key for chatbot

### Medium-term (Next Week)
1. Install and configure Qdrant
2. Implement vector search
3. Add authentication
4. Performance optimization

### Long-term (Next Month)
1. Production deployment
2. Docker containerization
3. CI/CD pipeline
4. Advanced analytics

---

## 📞 Support

### Common Commands Reference

```bash
# Start backend
cd f:\eytech
venv\Scripts\activate
uvicorn orchestrator.api.main:app --reload --port 8000

# Start frontend
cd f:\eytech\frontend
npm run dev

# Initialize database
python shared/database/init_db.py

# Seed data
python shared/database/seed_data.py

# Run tests
python tests/verify_all_modules.py

# Check database
psql -U postgres -d rfp_automation
```

---

## 🎉 Success!

If you've completed all steps, you now have:

✅ Fully functional RFP automation system  
✅ Database with sample data  
✅ Backend API running  
✅ Frontend connected  
✅ AI chatbot working  
✅ Email monitoring active  
✅ Auditor agent validating  

**Congratulations! Your system is ready for use!** 🚀

---

**Questions?** Check:
- `PROJECT_ANALYSIS.md` - Detailed project analysis
- `QUICK_STATUS.md` - Quick status overview
- `IMPLEMENTATION_STATUS.md` - Implementation details
- API Docs: http://localhost:8000/docs
