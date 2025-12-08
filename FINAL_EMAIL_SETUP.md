# 🎯 FINAL FIX - Email Inbox Complete Setup

## ⚡ Run These Commands in Order

```bash
# 1. Fix the database table
python fix_emails_table.py

# 2. Add sample emails
python add_sample_emails.py

# 3. Restart backend (to load updated API code)
# Press Ctrl+C in the backend terminal, then:
uvicorn orchestrator.api.main:app --reload --port 8000

# 4. Refresh browser
# Press F5 on Email Inbox page
```

---

## ✅ What Was Fixed

### **1. Database Schema** ✅
- Changed `processed BOOLEAN` → `processed_at TIMESTAMP`
- Table now matches what the code expects

### **2. Email API Routes** ✅
- Updated `/api/emails/list` to use `status` and `processed_at`
- Updated `/api/emails/{id}` to use correct columns
- Updated `/api/emails/stats` to use `status` instead of `processed`
- Fixed JSON parsing for attachments

### **3. Sales Agent** ✅
- Added `_save_email_to_db()` method
- Added `_update_email_status()` method
- Emails are now saved when processed

---

## 📧 Email Monitoring Status

### **Is It Working?**
**YES** - The background task is configured and will run automatically.

### **How It Works:**
1. **Backend starts** → Background task starts
2. **Every 1 hour** → Checks IMAP for new emails
3. **New email found** → Saves to database (status='pending')
4. **Downloads PDFs** → Saves to `f:\eytech\data\uploads\`
5. **Processes email** → Creates RFP
6. **Updates status** → status='processed', links RFP ID

### **Time to See Results:**
- **Sample Data:** Immediate (run `python add_sample_emails.py`)
- **Real Emails:** Up to 1 hour (next scheduled check)
- **Manual Trigger:** Can be triggered via API or script

---

## 🔧 Email Configuration

### **Required Settings in `.env`:**
```env
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### **Gmail Setup:**
1. Enable IMAP in Gmail settings
2. Create App Password (not your regular password)
3. Use App Password in `.env`

### **Outlook/Office365:**
```env
EMAIL_HOST=outlook.office365.com
EMAIL_PORT=993
```

---

## 📁 PDF Attachment Handling

### **Where PDFs Are Saved:**
```
f:\eytech\data\uploads\
```

### **Filename Format:**
```
{uuid}_{original_filename}.pdf
Example: a1b2c3d4_rfp_specifications.pdf
```

### **How It Works:**
1. Email has PDF attachment
2. PDF downloaded to `data/uploads/`
3. Full path stored in database: `["data/uploads/a1b2c3d4_rfp.pdf"]`
4. Visible in Email Inbox UI

---

## 🎯 What You'll See in Frontend

### **Email Inbox Page:**
- **Stats Cards:**
  - Total Emails: 5
  - Processed: 2
  - Total Attachments: 8

- **Email List:**
  - Subject lines
  - Sender emails
  - Timestamps ("2 days ago")
  - Status badges (Processed/Pending)
  - Attachment counts

- **Click Email:**
  - Full email body
  - Attachment list
  - Processing status
  - Linked RFP (if processed)

---

## 🔍 Verify Everything

### **1. Check Backend Logs:**
Look for:
```
INFO: Starting hourly email check...
INFO: Saved email to database: email-xxxxx
INFO: Updated email status: email-xxxxx -> processed
```

### **2. Check Database:**
```sql
psql -U rfp_user -d rfp_automation

SELECT email_id, subject, status, processed_at 
FROM emails 
ORDER BY received_at DESC;
```

### **3. Check API:**
```bash
# Test email list endpoint
curl http://localhost:8000/api/emails/list

# Should return JSON with emails array
```

### **4. Run Verification:**
```bash
python verify_system.py
```

---

## ⏱️ Email Monitoring Timeline

### **Automatic Checks:**
- **Frequency:** Every 1 hour (3600 seconds)
- **First Check:** When backend starts
- **Next Check:** 1 hour after first check
- **Continues:** As long as backend is running

### **Manual Trigger (Optional):**
You can create a script to trigger email check manually:

```python
from agents.sales.agent import SalesAgent

agent = SalesAgent()
rfps = agent.check_emails_imap()
print(f"Found {len(rfps)} new RFPs")
```

---

## 🚀 Quick Start (Complete Flow)

```bash
# 1. Fix database
python fix_emails_table.py

# 2. Add sample data
python add_sample_emails.py

# 3. Restart backend
# Ctrl+C, then:
uvicorn orchestrator.api.main:app --reload --port 8000

# 4. Open browser
# http://localhost:5173/emails

# 5. See 5 sample emails! ✅
```

---

## 📊 Expected Results

### **After Running Commands:**
```
✅ Database table fixed
✅ 5 sample emails added
✅ Backend restarted with updated code
✅ Email Inbox shows all emails
✅ Stats display correctly
✅ Emails are clickable
✅ Attachments are listed
```

### **After 1 Hour (Real Emails):**
```
✅ Background task checks IMAP
✅ New emails saved to database
✅ PDFs downloaded to data/uploads/
✅ RFPs created automatically
✅ Email status updated to 'processed'
✅ Visible in Email Inbox immediately
```

---

## 🐛 Troubleshooting

### **"500 Internal Server Error"**
- **Cause:** Backend not restarted after code changes
- **Fix:** Restart backend with `uvicorn` command

### **"No emails showing"**
- **Cause:** Sample data not added
- **Fix:** Run `python add_sample_emails.py`

### **"Email monitoring not working"**
- **Cause:** Email credentials not configured
- **Fix:** Update `.env` with correct IMAP settings

### **"PDFs not downloading"**
- **Cause:** `data/uploads/` directory doesn't exist
- **Fix:** Create directory: `mkdir -p data/uploads`

---

## ✨ Summary

**Current State:**
- ✅ Database schema fixed
- ✅ Email API updated
- ✅ Sales Agent saves emails
- ✅ Background monitoring configured
- ✅ PDF handling implemented

**Next Steps:**
1. Run `python fix_emails_table.py`
2. Run `python add_sample_emails.py`
3. Restart backend
4. Refresh browser
5. See emails working! 📬

**Time to Complete:** ~2 minutes

**Your Email Inbox will be fully functional!** 🎉
