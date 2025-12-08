# 📧 Fetch ALL Gmail Emails - Complete Guide

## ✅ Changes Made

### **1. Modified Sales Agent** ✅
Changed `agents/sales/agent.py` line 105:
- **Before:** `mail.search(None, "UNSEEN")` - Only unread emails
- **After:** `mail.search(None, "ALL")` - All emails

### **2. Created Fetch Script** ✅
Created `fetch_gmail_emails.py` - Smart email fetcher:
- Fetches emails from last 30 days (configurable)
- Limits to 10 most recent emails (configurable)
- Saves to database automatically
- Downloads PDF attachments
- Creates RFPs from email content
- Shows in Email Inbox immediately

---

## 🚀 Fetch Your Gmail Emails NOW

### **Option 1: Fetch Recent Emails (Recommended)**

```bash
# Fetch last 30 days, max 10 emails
python fetch_gmail_emails.py

# Fetch last 7 days, max 5 emails
python fetch_gmail_emails.py 7 5

# Fetch last 60 days, max 20 emails
python fetch_gmail_emails.py 60 20
```

### **Option 2: Fetch All Emails**

```bash
# This will fetch ALL 18 emails
python check_gmail_now.py
```

---

## 📊 What Happens When You Run It

### **Step-by-Step Process:**

1. **Connects to Gmail** via IMAP
2. **Searches for emails** (last 30 days by default)
3. **For each email:**
   - Extracts subject, sender, body
   - Downloads PDF/DOC attachments to `data/uploads/`
   - Saves email to database (status='pending')
   - Tries to create RFP from content
   - Updates status to 'processed' if RFP created
4. **Shows summary** of emails saved
5. **Emails appear in Email Inbox** immediately

---

## 🎯 Expected Output

```
============================================================
  📧 FETCHING GMAIL EMAILS
============================================================

📅 Fetching emails from last 30 days
📊 Maximum: 10 emails

🔍 Initializing Sales Agent...
📬 Connecting to Gmail IMAP...
🔎 Searching for emails since 09-Nov-2024...
📧 Found 18 emails
📥 Fetching 10 most recent emails...

  [1/10] ✅ Important: Your account statement...
  [2/10] ✅ Meeting reminder for tomorrow...
  [3/10] ✅ RFP for electrical equipment supply...
       🎯 Created RFP: RFP-2025-A1B2C3D4
  [4/10] ✅ Invoice #12345...
  ...

============================================================
  ✅ COMPLETED!
============================================================

📊 Summary:
  • Emails saved: 10
  • Emails skipped: 0
  • Total processed: 10

📬 Refresh your Email Inbox page to see the emails!
🌐 http://localhost:5173/emails
```

---

## 🔄 Verify Emails Are in Frontend

### **Step 1: Check Database**
```bash
python verify_system.py
```

Should show:
```
✅ Email List: OK
ℹ️  → 15 emails found  (5 sample + 10 Gmail)
```

### **Step 2: Check Email Inbox Page**
1. Open browser: `http://localhost:5173/emails`
2. Press F5 to refresh
3. You should see:
   - **Total Emails:** 15 (5 sample + 10 Gmail)
   - **Your Gmail emails** with real subjects, senders, dates
   - **Attachments** if any PDFs were in emails
   - **Status badges** (Processed/Pending)

### **Step 3: Click on an Email**
- See full email body
- See attachment list
- See if RFP was created

---

## 🗑️ Remove Sample Emails (Optional)

If you want to see only your Gmail emails:

```sql
psql -U rfp_user -d rfp_automation

DELETE FROM emails WHERE email_id LIKE 'email-00%';
```

Then refresh browser.

---

## ⚙️ Customization Options

### **Fetch Specific Date Range:**

```python
# Edit fetch_gmail_emails.py, line with mail.search:

# Last 7 days
status, messages = mail.search(None, '(SINCE "01-Dec-2024")')

# Specific date range
status, messages = mail.search(None, '(SINCE "01-Nov-2024" BEFORE "01-Dec-2024")')

# Only emails with attachments
status, messages = mail.search(None, '(SINCE "01-Dec-2024" HAS ATTACHMENT)')

# Only from specific sender
status, messages = mail.search(None, '(FROM "example@company.com")')
```

### **Fetch More/Less Emails:**

```bash
# Fetch last 90 days, max 50 emails
python fetch_gmail_emails.py 90 50

# Fetch last 7 days, max 3 emails
python fetch_gmail_emails.py 7 3
```

---

## 🔄 Automatic Background Fetching

### **Current Setup:**
- Background task runs **every 1 hour**
- Now fetches **ALL emails** (not just unread)
- Automatically saves to database
- Shows in Email Inbox

### **To Change Frequency:**

Edit `orchestrator/api/main.py`, line 66:

```python
# Every 30 minutes
await asyncio.sleep(1800)

# Every 2 hours
await asyncio.sleep(7200)

# Every 6 hours
await asyncio.sleep(21600)
```

Then restart backend.

---

## 📁 Attachment Handling

### **Supported File Types:**
- PDF (.pdf)
- Word (.doc, .docx)

### **Storage Location:**
```
f:\eytech\data\uploads\
```

### **Filename Format:**
```
{uuid}_{original_name}.pdf
Example: a1b2c3d4_quotation.pdf
```

### **In Database:**
Stored as JSON array:
```json
["data/uploads/a1b2c3d4_quotation.pdf", "data/uploads/e5f6g7h8_specs.pdf"]
```

### **In Frontend:**
- Attachment count shown in email list
- Full list shown when clicking email
- Future: Add download links

---

## 🎯 Quick Commands Reference

```bash
# Test Gmail connection
python test_gmail_connection.py

# Fetch recent emails (recommended)
python fetch_gmail_emails.py

# Fetch all emails
python check_gmail_now.py

# Fetch custom range
python fetch_gmail_emails.py 7 5

# Verify system
python verify_system.py

# Check database
psql -U rfp_user -d rfp_automation -c "SELECT COUNT(*) FROM emails;"
```

---

## ✅ Checklist

- [x] Gmail connection working
- [x] Modified code to fetch ALL emails
- [x] Created fetch script
- [ ] Run `python fetch_gmail_emails.py`
- [ ] Refresh Email Inbox page
- [ ] See your Gmail emails! ✅

---

## 🎉 Summary

**Before:**
- ❌ Only fetched unread emails
- ❌ 0 emails found (all were read)

**After:**
- ✅ Fetches ALL emails (or recent emails)
- ✅ Configurable date range and limits
- ✅ Saves to database automatically
- ✅ Shows in Email Inbox immediately
- ✅ Downloads PDF attachments

**Run:** `python fetch_gmail_emails.py`

**Result:** Your Gmail emails will appear in Email Inbox! 📬✨
