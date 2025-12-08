# ✅ Setup Checklist - RFP Automation System

**Use this checklist to track your setup progress**

---

## 📋 Pre-Setup Questions

### Question 1: PostgreSQL
- [ ] I have PostgreSQL installed
  - Password for `postgres` user: ________________
- [ ] I need to install PostgreSQL
  - [ ] Downloaded installer
  - [ ] Installed PostgreSQL
  - [ ] Noted password: ________________

### Question 2: Google API Key (Optional)
- [ ] I have a Google API key
  - API Key: ________________
- [ ] I need to get one → https://makersuite.google.com/app/apikey
- [ ] Skip for now (chatbot won't work)

### Question 3: Email Monitoring (Optional)
- [ ] I want email monitoring
  - Email: ________________
  - App Password: ________________
- [ ] Skip for now

---

## 🚀 Setup Steps

### Step 1: Environment Configuration
- [ ] Copied `.env.template` to `.env`
- [ ] Updated `DB_PASSWORD` in `.env`
- [ ] Updated `GOOGLE_API_KEY` in `.env` (if applicable)
- [ ] Updated email credentials in `.env` (if applicable)

### Step 2: Python Setup
- [ ] Created virtual environment: `python -m venv venv`
- [ ] Activated venv: `venv\Scripts\activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] All packages installed successfully

### Step 3: Database Initialization
- [ ] PostgreSQL service is running
- [ ] Ran: `python shared/database/init_db.py`
- [ ] Database `rfp_automation` created
- [ ] All 7 tables created
- [ ] No errors in output

### Step 4: Data Seeding
- [ ] Ran: `python shared/database/seed_data.py`
- [ ] 6 products loaded
- [ ] 3 sample RFPs loaded
- [ ] Metrics initialized
- [ ] No errors in output

### Step 5: Backend Startup
- [ ] Ran: `uvicorn orchestrator.api.main:app --reload --port 8000`
- [ ] Server started successfully
- [ ] Visited: http://localhost:8000/docs
- [ ] API documentation loads
- [ ] Health check passes: http://localhost:8000/health

### Step 6: Frontend Setup
- [ ] Opened new terminal
- [ ] Navigated to: `cd frontend`
- [ ] Ran: `npm install`
- [ ] All packages installed
- [ ] Ran: `npm run dev`
- [ ] Server started on http://localhost:5173

### Step 7: Frontend Connection
- [ ] Opened: `frontend/src/services/api.js`
- [ ] Changed: `USE_MOCK_DATA = false`
- [ ] Saved file
- [ ] Refreshed browser
- [ ] Frontend connected to backend

---

## 🧪 Verification Tests

### Test 1: Database Connection
- [ ] Can connect to PostgreSQL
- [ ] Database `rfp_automation` exists
- [ ] Can query products table
- [ ] Can query rfps table

### Test 2: Backend API
- [ ] API docs accessible
- [ ] Can GET /api/products/list
- [ ] Can GET /api/rfp/list
- [ ] Can GET /api/analytics/dashboard
- [ ] Health check returns "healthy"

### Test 3: Frontend
- [ ] Dashboard loads
- [ ] Can navigate to all pages
- [ ] Submit RFP page works
- [ ] Can see sample products
- [ ] Analytics page shows charts

### Test 4: End-to-End Flow
- [ ] Submitted RFP via frontend
- [ ] Specs extracted correctly
- [ ] Products matched
- [ ] Pricing calculated
- [ ] RFP saved to database
- [ ] Can view RFP in list

### Test 5: Chatbot (If API key provided)
- [ ] Chat widget appears (bottom right)
- [ ] Can open chat
- [ ] Can send message
- [ ] Receives response from Gemini
- [ ] Chat history maintained

### Test 6: Email Monitoring (If configured)
- [ ] Backend logs show email check
- [ ] No connection errors
- [ ] Can discover RFPs from email

---

## 🐛 Troubleshooting Checklist

### If Database Connection Fails
- [ ] PostgreSQL service is running
- [ ] Password in `.env` is correct
- [ ] Port 5432 is not blocked
- [ ] Database name is correct

### If Backend Won't Start
- [ ] Virtual environment is activated
- [ ] All dependencies installed
- [ ] No port 8000 conflicts
- [ ] `.env` file exists
- [ ] Check error logs

### If Frontend Shows Errors
- [ ] Backend is running
- [ ] `USE_MOCK_DATA` setting is correct
- [ ] CORS is configured
- [ ] Check browser console (F12)

### If Chatbot Doesn't Work
- [ ] `GOOGLE_API_KEY` in `.env`
- [ ] API key is valid
- [ ] Backend restarted after adding key
- [ ] Check backend logs

---

## 📊 Feature Status

### Core Features
- [ ] RFP submission works
- [ ] Spec extraction works
- [ ] Product matching works
- [ ] Pricing calculation works
- [ ] Data persists in database

### Advanced Features
- [ ] Chatbot responds
- [ ] Email monitoring active
- [ ] Analytics dashboard shows data
- [ ] Auditor validation works

---

## ✅ Completion Checklist

- [ ] All setup steps completed
- [ ] All verification tests passed
- [ ] No errors in logs
- [ ] Can submit and view RFPs
- [ ] System is ready for use

---

## 📝 Notes

**Issues Encountered:**
_Write any issues you faced here_

**Solutions Applied:**
_Write what fixed the issues_

**Next Steps:**
_What you plan to do next_

---

## 🎉 Success Criteria

You're done when:
✅ Backend runs without errors
✅ Frontend loads successfully  
✅ Can submit RFP and see results  
✅ Data saves to database  
✅ All pages are accessible  

**Congratulations! Your RFP Automation System is live!** 🚀

---

**Need Help?** Check:
- `SETUP_GUIDE.md` - Detailed instructions
- `PROJECT_ANALYSIS.md` - System overview
- `IMPLEMENTATION_PROGRESS.md` - What's implemented
- API Docs: http://localhost:8000/docs
