# 🗄️ Database Migration Guide - Fix "emails table does not exist"

**Error:** `relation "emails" does not exist`  
**Solution:** Run database migration to create new tables

---

## 🚀 **Quick Fix (Choose One Method)**

### **Method 1: Using psql Command** (Recommended)

```bash
# Open new terminal
cd f:\eytech

# Run migration
psql -U postgres -d rfp_automation -f quick_migration.sql
```

**Expected Output:**
```
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
✅ Migration complete! Tables created successfully.
```

---

### **Method 2: Using Python Script**

```bash
# In your venv terminal
cd f:\eytech
venv\Scripts\activate
python run_migration.py
```

---

### **Method 3: Manual SQL (If above don't work)**

1. **Connect to PostgreSQL:**
```bash
psql -U postgres -d rfp_automation
```

2. **Run these commands:**
```sql
-- Create emails table
CREATE TABLE IF NOT EXISTS emails (
    email_id VARCHAR(50) PRIMARY KEY,
    subject TEXT NOT NULL,
    sender VARCHAR(255),
    received_at TIMESTAMP,
    body TEXT,
    attachments JSONB,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_emails_status ON emails(status);
CREATE INDEX idx_emails_rfp_id ON emails(rfp_id);
CREATE INDEX idx_emails_received_at ON emails(received_at);

-- Create audit_reports table
CREATE TABLE IF NOT EXISTS audit_reports (
    audit_id VARCHAR(50) PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE CASCADE,
    audit_timestamp TIMESTAMP DEFAULT NOW(),
    overall_recommendation VARCHAR(20) NOT NULL,
    compliance_score FLOAT,
    critical_issues_count INTEGER DEFAULT 0,
    summary TEXT,
    rfp_validation JSONB,
    match_validation JSONB,
    pricing_validation JSONB,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_rfp_id ON audit_reports(rfp_id);
CREATE INDEX idx_audit_timestamp ON audit_reports(audit_timestamp);
CREATE INDEX idx_audit_recommendation ON audit_reports(overall_recommendation);

-- Verify
SELECT 'emails' as table_name, COUNT(*) as row_count FROM emails
UNION ALL
SELECT 'audit_reports' as table_name, COUNT(*) as row_count FROM audit_reports;
```

3. **Exit:**
```sql
\q
```

---

## ✅ **Verify Migration**

After running migration, verify tables exist:

```bash
psql -U postgres -d rfp_automation -c "\dt"
```

**Expected output should include:**
```
 public | emails              | table | postgres
 public | audit_reports       | table | postgres
 public | rfps                | table | postgres
 public | products            | table | postgres
```

---

## 🔄 **After Migration**

### **1. Refresh Frontend**
```
Press F5 in browser or Ctrl+R
```

### **2. Check Email Inbox**
```
http://localhost:5173/emails
```
Should now show empty state (no errors)

### **3. Check Auditor Dashboard**
```
http://localhost:5173/auditor
```
Should now show empty state (no errors)

---

## 📊 **What Gets Created**

### **emails table:**
- Stores discovered emails from monitoring
- Tracks PDF attachments
- Links to created RFPs
- Status tracking (pending/processed)

### **audit_reports table:**
- Stores audit history
- Compliance scores
- Recommendations (APPROVE/REVIEW/REJECT)
- Critical issues tracking

---

## 🎯 **Quick Test After Migration**

### **Test 1: Check Tables**
```bash
psql -U postgres -d rfp_automation -c "SELECT COUNT(*) FROM emails;"
psql -U postgres -d rfp_automation -c "SELECT COUNT(*) FROM audit_reports;"
```

**Expected:** Both should return `0` (empty tables)

### **Test 2: Check Frontend**
1. Open http://localhost:5173/emails
2. Should see: "Total Emails: 0"
3. No errors in console

### **Test 3: Check API**
```bash
curl http://localhost:8000/api/emails/list
```

**Expected:**
```json
{
  "emails": [],
  "total": 0,
  "processed_count": 0,
  "pending_count": 0
}
```

---

## 🐛 **Troubleshooting**

### **Error: "permission denied"**
```bash
# Run as postgres superuser
psql -U postgres -d rfp_automation -f quick_migration.sql
```

### **Error: "database does not exist"**
```bash
# Create database first
psql -U postgres -c "CREATE DATABASE rfp_automation;"

# Then run migration
psql -U postgres -d rfp_automation -f quick_migration.sql
```

### **Error: "psql command not found"**
```bash
# Add PostgreSQL to PATH or use full path
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d rfp_automation -f quick_migration.sql
```

---

## 📝 **Files Created**

1. ✅ `quick_migration.sql` - Quick migration script
2. ✅ `run_migration.py` - Python migration script

---

## 🎊 **Summary**

**Problem:** Database missing `emails` and `audit_reports` tables

**Solution:** Run migration with one of these:
```bash
# Option 1 (Easiest)
psql -U postgres -d rfp_automation -f quick_migration.sql

# Option 2
python run_migration.py

# Option 3
# Copy-paste SQL from Method 3 above
```

**Result:** 
- ✅ Tables created
- ✅ Frontend works
- ✅ No more errors
- ✅ System ready!

---

**Run the migration and your system will be 100% functional!** 🚀
