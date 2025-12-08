# 🚀 Quick Database Fix - Copy & Paste Solution

## ✅ **Easiest Method - Copy & Paste SQL**

### **Step 1: Open PostgreSQL**
```bash
psql -U postgres -d rfp_automation
```

### **Step 2: Copy & Paste This (All at once)**

```sql
-- Create emails table
CREATE TABLE IF NOT EXISTS emails (
    email_id VARCHAR(50) PRIMARY KEY,
    subject TEXT NOT NULL,
    sender VARCHAR(255),
    received_at TIMESTAMP,
    body TEXT,
    attachments JSONB,
    rfp_id VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for emails
CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status);
CREATE INDEX IF NOT EXISTS idx_emails_rfp_id ON emails(rfp_id);
CREATE INDEX IF NOT EXISTS idx_emails_received_at ON emails(received_at);

-- Create audit_reports table
CREATE TABLE IF NOT EXISTS audit_reports (
    audit_id VARCHAR(50) PRIMARY KEY,
    rfp_id VARCHAR(50),
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

-- Create indexes for audit_reports
CREATE INDEX IF NOT EXISTS idx_audit_rfp_id ON audit_reports(rfp_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_reports(audit_timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_recommendation ON audit_reports(overall_recommendation);

-- Verify tables created
SELECT 'emails' as table_name, COUNT(*) as rows FROM emails
UNION ALL
SELECT 'audit_reports' as table_name, COUNT(*) as rows FROM audit_reports;
```

### **Step 3: Exit**
```sql
\q
```

---

## ✅ **Expected Output**

After pasting the SQL, you should see:

```
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX

 table_name    | rows
---------------+------
 emails        |    0
 audit_reports |    0
(2 rows)
```

---

## 🎯 **After Running SQL**

1. **Refresh your browser** (F5 or Ctrl+R)
2. **Go to Email Inbox:** http://localhost:5173/emails
3. **Go to Auditor Dashboard:** http://localhost:5173/auditor

**Both should now work!** ✅

---

## 🐛 **If psql command not found**

### **Windows:**
```bash
# Find PostgreSQL installation
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d rfp_automation

# Or add to PATH and restart terminal
```

### **Alternative: Use pgAdmin**
1. Open pgAdmin
2. Connect to `rfp_automation` database
3. Open Query Tool
4. Paste the SQL from Step 2
5. Click Execute (F5)

---

## 📊 **Verify It Worked**

### **Check in terminal:**
```bash
psql -U postgres -d rfp_automation -c "\dt"
```

**Should show:**
```
 public | emails              | table | postgres
 public | audit_reports       | table | postgres
```

### **Check in browser:**
- http://localhost:5173/emails → Should show "Total Emails: 0"
- http://localhost:5173/auditor → Should show "Total Audits: 0"

---

## 🎉 **That's It!**

**Just 3 steps:**
1. Open psql
2. Paste SQL
3. Refresh browser

**Your system will be 100% functional!** 🚀
