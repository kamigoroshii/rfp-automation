# 📧 Gmail Integration Setup Guide

## 🎯 Current Status

✅ **Email Inbox UI:** Working perfectly
✅ **Database:** 5 sample emails showing
✅ **Background Task:** Running every hour
❌ **Gmail Connection:** Not configured yet

---

## 🔧 How to Connect Your Gmail

### **Step 1: Enable IMAP in Gmail**

1. Go to Gmail Settings (⚙️ icon)
2. Click "See all settings"
3. Go to "Forwarding and POP/IMAP" tab
4. Enable IMAP
5. Save Changes

### **Step 2: Create Gmail App Password**

**Important:** You CANNOT use your regular Gmail password. You need an "App Password".

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)
3. Go to https://myaccount.google.com/apppasswords
4. Select "Mail" and "Windows Computer"
5. Click "Generate"
6. **Copy the 16-character password** (e.g., `abcd efgh ijkl mnop`)

### **Step 3: Update .env File**

Open `f:\eytech\.env` and add/update these lines:

```env
# Email Configuration
EMAIL_HOST=imap.gmail.com
EMAIL_PORT=993
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
```

**Replace:**
- `your-email@gmail.com` with your actual Gmail address
- `abcdefghijklmnop` with the App Password (remove spaces)

### **Step 4: Restart Backend**

```bash
# Press Ctrl+C in backend terminal
# Then restart:
uvicorn orchestrator.api.main:app --reload --port 8000
```

### **Step 5: Wait or Trigger Manually**

**Option A: Wait (Automatic)**
- Background task runs every 1 hour
- Next check will fetch your Gmail emails
- They'll appear in Email Inbox automatically

**Option B: Trigger Now (Manual)**
Create a file `check_gmail_now.py`:

```python
from agents.sales.agent import SalesAgent

print("🔍 Checking Gmail for new RFPs...")
agent = SalesAgent()
rfps = agent.check_emails_imap()

print(f"\n✅ Found {len(rfps)} new RFPs from Gmail")
print("📬 Check your Email Inbox page!")
```

Then run:
```bash
python check_gmail_now.py
```

---

## 📊 What Happens When Gmail is Connected

### **Automatic Process:**
1. **Every hour**, background task checks Gmail
2. **Fetches UNSEEN emails** (unread emails)
3. **For each email:**
   - Saves to database (status='pending')
   - Downloads PDF/DOC attachments to `data/uploads/`
   - Processes email content
   - Creates RFP if it's RFP-related
   - Updates status to 'processed'
   - Links to RFP ID

### **What You'll See:**
- **Email Inbox:** All your Gmail emails
- **Attachments:** PDFs downloaded and listed
- **RFPs:** Automatically created from emails
- **Status:** Shows which emails were processed

---

## 🔍 Verify Gmail Connection

### **Check 1: Test Connection**

Create `test_gmail_connection.py`:

```python
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('EMAIL_HOST')
user = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASSWORD')

print(f"Testing connection to {host}...")
print(f"User: {user}")

try:
    mail = imaplib.IMAP4_SSL(host)
    mail.login(user, password)
    mail.select("inbox")
    
    status, messages = mail.search(None, "ALL")
    email_count = len(messages[0].split())
    
    print(f"✅ Connection successful!")
    print(f"📧 Found {email_count} emails in inbox")
    
    mail.close()
    mail.logout()
except Exception as e:
    print(f"❌ Connection failed: {str(e)}")
```

Run:
```bash
python test_gmail_connection.py
```

### **Check 2: Backend Logs**

Look for these messages in backend terminal:
```
INFO: Starting hourly email check...
INFO: Connecting to IMAP server: imap.gmail.com
INFO: Saved email to database: email-xxxxx
INFO: Found X new RFPs from email
```

---

## 🎯 Sample vs Real Emails

### **Sample Emails (Current):**
- ✅ 5 test emails
- ✅ Show UI functionality
- ✅ Safe to delete anytime
- ❌ Not from your Gmail

### **Real Gmail Emails (After Setup):**
- ✅ Your actual emails
- ✅ Real attachments
- ✅ Automatic processing
- ✅ RFP creation

---

## 🗑️ Clear Sample Emails (Optional)

If you want to remove the sample emails:

```sql
psql -U rfp_user -d rfp_automation

DELETE FROM emails WHERE email_id LIKE 'email-00%';
```

Then refresh Email Inbox page.

---

## ⏱️ Timeline

### **After Gmail Configuration:**

| Time | What Happens |
|------|--------------|
| 0 min | Configure .env, restart backend |
| 0-60 min | Wait for next hourly check |
| 60 min | Background task checks Gmail |
| 60 min | Emails saved to database |
| 60 min | Visible in Email Inbox |

**Or use manual trigger to see emails immediately!**

---

## 🐛 Troubleshooting

### **"Authentication failed"**
- Make sure you're using **App Password**, not regular password
- Remove spaces from App Password
- Check EMAIL_USER is correct

### **"Connection refused"**
- Check EMAIL_HOST is `imap.gmail.com`
- Check EMAIL_PORT is `993`
- Verify IMAP is enabled in Gmail

### **"No new emails found"**
- Background task only fetches **UNSEEN** (unread) emails
- Mark some emails as unread in Gmail
- Or modify code to fetch all emails

### **"Emails not showing in UI"**
- Check backend logs for errors
- Verify database has emails: `SELECT COUNT(*) FROM emails;`
- Refresh browser (F5)

---

## 📝 Quick Setup Checklist

- [ ] Enable IMAP in Gmail settings
- [ ] Create Gmail App Password
- [ ] Update `.env` file with credentials
- [ ] Restart backend
- [ ] Wait 1 hour OR run manual trigger
- [ ] Check Email Inbox page
- [ ] See your Gmail emails! ✅

---

## ✨ Summary

**Current State:**
- ✅ Email Inbox working with sample data
- ❌ Gmail not connected yet

**To Connect Gmail:**
1. Get Gmail App Password
2. Update `.env` file
3. Restart backend
4. Wait or trigger manually

**Time to Setup:** ~5 minutes
**Time to See Emails:** Immediate (manual) or 1 hour (automatic)

---

**Your Email Inbox is ready - just needs Gmail credentials!** 📬🔐
