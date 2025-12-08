# 📧 Email Inbox Status & System Verification

## ❓ Why Are Emails Not Showing?

Your Email Inbox is currently **empty** for these reasons:

### 1. **Database Table Not Created Yet** 
The `emails` table doesn't exist in your PostgreSQL database. This table is required to store email data.

### 2. **No Email Processing Yet**
The Sales Agent hasn't been configured to automatically save emails to the database when processing them.

### 3. **No Sample Data**
There's no test/sample data in the system yet.

---

## ✅ Solution: 3 Simple Steps

### **Step 1: Run Database Migration**

Open a terminal in `f:\eytech` and run:

```bash
python run_migration.py
```

This creates the `emails` and `audit_reports` tables.

**What it does:**
- Creates `emails` table with columns: email_id, subject, sender, received_at, body, attachments, status, processed_at
- Creates `audit_reports` table for auditor data
- Uses `IF NOT EXISTS` so it's safe to run multiple times

---

### **Step 2: Verify System Health**

Run the verification script I just created:

```bash
python verify_system.py
```

**Or on Windows, double-click:**
```
verify.bat
```

**This checks:**
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:5173
- ✅ All API endpoints responding
- ✅ Database tables exist
- ✅ Data counts for each module

---

### **Step 3: Add Sample Email Data (Optional)**

To see emails immediately without waiting for real email processing:

**Option A: Using SQL**
```sql
psql -U rfp_user -d rfp_automation

INSERT INTO emails (email_id, subject, sender, received_at, body, attachments, status, processed_at)
VALUES 
  ('email-001', 'RFP for 11kV Cable Supply - Urgent', 'procurement@powergrid.com', NOW() - INTERVAL '2 days', 
   'Dear Supplier, We require 500 meters of 11kV XLPE cable for our substation project. Please provide quotation.', 
   '["rfp_cable.pdf"]', 'processed', NOW() - INTERVAL '1 day'),
  
  ('email-002', '100kVA Transformer Quotation Request', 'buyer@electricco.in', NOW() - INTERVAL '1 day', 
   'We need pricing for 100kVA distribution transformer. Specifications attached.', 
   '["transformer_specs.pdf"]', 'processed', NOW()),
  
  ('email-003', 'Tender Notice - Electrical Equipment Supply', 'tender@govt.in', NOW() - INTERVAL '3 hours', 
   'Government tender for electrical equipment supply. Deadline: 15 days.', 
   '["tender_document.pdf", "technical_specs.xlsx"]', 'pending', NULL),
  
  ('email-004', 'Re: Cable Testing Requirements', 'quality@testlab.com', NOW() - INTERVAL '1 hour', 
   'Please confirm testing requirements for the cable samples.', 
   '[]', 'pending', NULL);
```

**Option B: Using Python Script**

I can create a quick script to populate sample data if you prefer.

---

## 🔍 Verification Script Features

The `verify_system.py` script I created checks:

### **Backend Health**
- ✅ Server is running
- ✅ Health endpoint responding
- ✅ Database connection working

### **Frontend Health**
- ✅ Development server running
- ✅ Page accessible

### **API Endpoints**
- ✅ `/api/rfp/list` - RFP listing
- ✅ `/api/analytics/dashboard` - Analytics data
- ✅ `/api/products/search` - Product search
- ✅ `/api/emails/list` - **Email listing** ← This is what you need
- ✅ `/api/auditor/reports` - Auditor reports

### **Database Tables**
- ✅ `rfps` table exists
- ✅ `emails` table exists (after migration)
- ✅ `audit_reports` table exists (after migration)
- ✅ Data counts for each table

### **Report Generation**
- 📊 Overall system health score
- 📝 Specific recommendations
- ⚠️  Warnings for missing components

---

## 🎯 Expected Results After Setup

### **Before Migration:**
```
❌ Emails table might not exist or is inaccessible
ℹ️  Run: python run_migration.py
```

### **After Migration (No Data):**
```
✅ Emails table exists (0 records)
⚠️  Email inbox is empty - add sample data or configure email agent
```

### **After Adding Sample Data:**
```
✅ Emails table exists (4 records)
✅ Email List: OK
ℹ️  → 4 emails found
```

---

## 📱 How to Use the Email Inbox

Once you have data:

1. **Navigate to Email Inbox** (http://localhost:5173/emails)

2. **You'll see:**
   - **Stats Cards:**
     - Total Emails
     - Processed Emails  
     - Total Attachments
   
   - **Email List:**
     - Subject line
     - Sender email
     - Received timestamp
     - Status badge (Processed/Pending)
     - Attachment count

3. **Click on an email** to view:
   - Full email body
   - Attachment list
   - Processing status
   - Related RFP (if processed)

---

## 🔄 Real Email Processing (Future)

To process **real emails** from your inbox:

### **Configure Email Settings**

Update `.env` file:
```env
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### **Update Sales Agent**

The Sales Agent (`agents/sales/agent.py`) needs to be modified to:
1. Fetch emails from IMAP
2. Extract RFP information
3. **Save to `emails` table** ← Currently missing
4. Process attachments
5. Create RFP entries

This is a **future enhancement** - for now, use sample data to test the UI.

---

## 🚀 Quick Start Commands

```bash
# 1. Run migration
python run_migration.py

# 2. Verify system
python verify_system.py

# 3. Add sample data (optional)
psql -U rfp_user -d rfp_automation -c "INSERT INTO emails ..."

# 4. Refresh browser
# Press F5 on Email Inbox page
```

---

## 📞 Troubleshooting

### **"Backend not running"**
```bash
uvicorn orchestrator.api.main:app --reload --port 8000
```

### **"Frontend not running"**
```bash
cd frontend
npm run dev
```

### **"Database connection failed"**
- Check PostgreSQL is running
- Verify `.env` credentials
- Test: `psql -U rfp_user -d rfp_automation`

### **"Migration failed"**
- Check database exists: `psql -U rfp_user -l`
- Create if missing: `createdb -U rfp_user rfp_automation`
- Run migration again

---

## ✨ Summary

**Current State:** Email Inbox UI is ready, but database table is missing

**Action Required:** Run `python run_migration.py`

**Optional:** Add sample data to see emails immediately

**Verification:** Run `python verify_system.py` to check everything

**Result:** Fully functional Email Inbox! 📬

---

**Created:** 2025-12-08  
**Files Created:**
- `verify_system.py` - System verification script
- `verify.bat` - Windows batch runner
- `EMAIL_INBOX_SETUP.md` - This guide
