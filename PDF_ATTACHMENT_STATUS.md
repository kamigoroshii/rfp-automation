# 📎 PDF Attachment Flow - Complete Status

## ✅ What's Working

### **1. Email Processing with PDFs** ✅
When an email with PDF attachment is received:

```
Email → Extract PDF → Save to data/uploads/ → Store path in email record
```

**Code Location:** `agents/sales/agent.py` lines 153-166
- ✅ PDFs are downloaded from email
- ✅ Saved to `f:\eytech\data\uploads\`
- ✅ Filename format: `{uuid}_{original_name}.pdf`
- ✅ Path stored in email's `attachments` JSON field

### **2. Email Database Storage** ✅
**Table:** `emails`
- ✅ `attachments` column (JSONB)
- ✅ Stores array of file paths
- ✅ Example: `["data/uploads/a1b2c3d4_rfp.pdf"]`

### **3. Email Inbox Display** ✅
**Frontend:** `frontend/src/pages/EmailInbox.jsx`
- ✅ Shows attachment count
- ✅ Displays in email list
- ✅ Visible when clicking email

---

## ⚠️ What's NOT Working

### **1. RFP Table Missing Attachments Column** ❌

**Problem:**
- RFPs are created from emails
- Attachments are in `RFPSummary` object (line 277)
- But `rfps` table doesn't have `attachments` column
- INSERT statement doesn't include attachments (line 192-205)

**Impact:**
- ❌ PDFs are saved to disk
- ❌ PDFs are linked to emails
- ❌ But NOT linked to RFPs in database
- ❌ RFP Detail page won't show attachments

### **2. RFP Detail Page Not Showing Attachments** ❌

**Frontend:** `frontend/src/pages/RFPDetail.jsx`
- Currently doesn't display attachments
- No UI component for attachment list
- No download links

---

## 🔧 How to Fix

### **Step 1: Add Attachments Column to RFPs Table**

Create `add_rfp_attachments.py`:

```python
"""
Add attachments column to rfps table
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'rfp_automation'),
    'user': os.getenv('DB_USER', 'rfp_user'),
    'password': os.getenv('DB_PASSWORD', 'rfp_password')
}

def add_attachments_column():
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔨 Adding attachments column to rfps table...")
        cursor.execute("""
            ALTER TABLE rfps 
            ADD COLUMN IF NOT EXISTS attachments JSONB DEFAULT '[]'::jsonb
        """)
        
        print("✅ Attachments column added successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    add_attachments_column()
```

### **Step 2: Update RFP Service to Save Attachments**

Modify `orchestrator/services/rfp_service.py` line 192:

```python
cursor.execute("""
    INSERT INTO rfps 
    (rfp_id, title, source, deadline, scope, testing_requirements, 
     discovered_at, status, attachments)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    rfp_summary.rfp_id,
    rfp_summary.title,
    rfp_summary.source,
    rfp_summary.deadline,
    rfp_summary.scope,
    rfp_summary.testing_requirements,
    rfp_summary.discovered_at,
    rfp_summary.status,
    json.dumps(rfp_summary.attachments)  # ADD THIS
))
```

### **Step 3: Update RFP Detail Page to Show Attachments**

Add to `frontend/src/pages/RFPDetail.jsx`:

```jsx
{/* Attachments Section */}
{attachments && attachments.length > 0 && (
  <div className="bg-white rounded-lg shadow-md p-6">
    <h3 className="text-xl font-bold text-text mb-4">Attachments</h3>
    <div className="space-y-2">
      {attachments.map((attachment, idx) => (
        <div key={idx} className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
          <FileText size={20} className="text-primary" />
          <div className="flex-1">
            <p className="text-sm font-medium text-text">
              {attachment.split('/').pop()}
            </p>
            <p className="text-xs text-text-light">
              {attachment}
            </p>
          </div>
          <a
            href={`http://localhost:8000/uploads/${attachment.split('/').pop()}`}
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1 bg-primary text-white rounded text-sm hover:bg-primary-light"
          >
            Download
          </a>
        </div>
      ))}
    </div>
  </div>
)}
```

### **Step 4: Add Static File Serving for Uploads**

Add to `orchestrator/api/main.py`:

```python
from fastapi.staticfiles import StaticFiles

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="data/uploads"), name="uploads")
```

---

## 📊 Current Flow vs Desired Flow

### **Current Flow:**
```
Email with PDF
  ↓
Save PDF to data/uploads/ ✅
  ↓
Store path in emails.attachments ✅
  ↓
Create RFP from email ✅
  ↓
Save RFP to database ❌ (no attachments)
  ↓
Display in RFP List ✅
  ↓
Click RFP Detail ❌ (no attachments shown)
```

### **Desired Flow:**
```
Email with PDF
  ↓
Save PDF to data/uploads/ ✅
  ↓
Store path in emails.attachments ✅
  ↓
Create RFP from email ✅
  ↓
Save RFP with attachments to database ✅ (after fix)
  ↓
Display in RFP List ✅
  ↓
Click RFP Detail ✅ (attachments shown with download links)
```

---

## 🎯 Quick Fix Implementation

I'll create the necessary files to fix this:

1. **`add_rfp_attachments_column.py`** - Add column to database
2. **Update `rfp_service.py`** - Save attachments
3. **Update `RFPDetail.jsx`** - Display attachments
4. **Update `main.py`** - Serve uploaded files

---

## ✅ Verification Steps

After implementing fixes:

### **1. Check Database**
```sql
psql -U rfp_user -d rfp_automation

-- Check if column exists
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'rfps' AND column_name = 'attachments';

-- Check RFP with attachments
SELECT rfp_id, title, attachments 
FROM rfps 
WHERE attachments IS NOT NULL AND attachments != '[]'::jsonb;
```

### **2. Test Email with PDF**
1. Send test email with PDF to your Gmail
2. Run `python fetch_gmail_emails.py`
3. Check `data/uploads/` for PDF file
4. Check database for RFP with attachments
5. Open RFP Detail page
6. See attachments section with download link

### **3. Verify Frontend**
1. Go to RFP List
2. Click on RFP created from email
3. Scroll to Attachments section
4. See PDF listed
5. Click Download
6. PDF opens in new tab

---

## 📝 Summary

**Current State:**
- ✅ PDFs downloaded from emails
- ✅ Saved to `data/uploads/`
- ✅ Linked to emails in database
- ✅ Shown in Email Inbox
- ❌ NOT linked to RFPs in database
- ❌ NOT shown in RFP Detail page

**After Fix:**
- ✅ Everything above PLUS
- ✅ PDFs linked to RFPs in database
- ✅ Shown in RFP Detail page
- ✅ Download links working

**Time to Implement:** ~10 minutes

---

**Let me implement these fixes now!** 🔧
