# 📧 Email Inbox Setup Guide

## Why Your Email Inbox Is Empty

The Email Inbox page is currently empty because:

### 1. **Database Table Missing** ❌
The `emails` table hasn't been created yet in your PostgreSQL database.

### 2. **No Email Processing** ❌
The Sales Agent hasn't been configured to save emails to the database.

---

## 🚀 Quick Fix: Get Emails Showing

### Step 1: Run Database Migration

```bash
python run_migration.py
```

This will create the `emails` and `audit_reports` tables.

**Alternative (if Python script fails):**
```bash
psql -U rfp_user -d rfp_automation -f quick_migration.sql
```

### Step 2: Verify Tables Were Created

Run the verification script:
```bash
python verify_system.py
```

This will check if all systems are working correctly.

### Step 3: Add Sample Email Data (Optional)

To see the Email Inbox in action immediately, you can add sample data:

```sql
-- Connect to database
psql -U rfp_user -d rfp_automation

-- Insert sample emails
INSERT INTO emails (email_id, subject, sender, received_at, body, attachments, status, processed_at)
VALUES 
  ('email-001', 'RFP for 11kV Cable Supply', 'procurement@example.com', NOW() - INTERVAL '2 days', 'We need 500m of 11kV XLPE cable...', '[]', 'processed', NOW() - INTERVAL '1 day'),
  ('email-002', 'Transformer Quotation Request', 'buyer@company.com', NOW() - INTERVAL '1 day', 'Please quote for 100kVA transformer...', '["rfp.pdf"]', 'processed', NOW()),
  ('email-003', 'New RFP - Electrical Equipment', 'tender@govt.in', NOW(), 'Tender for electrical equipment supply...', '["tender_doc.pdf"]', 'pending', NULL);
```

### Step 4: Configure Email Agent (For Real Emails)

To process real emails from your inbox, update the Sales Agent configuration:

**File:** `agents/sales/agent.py`

Add this method call in the email processing function to save to database:

```python
def save_email_to_db(self, email_data):
    """Save processed email to database"""
    from shared.database.connection import get_db_manager
    
    db = get_db_manager()
    if db:
        with db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO emails (email_id, subject, sender, received_at, body, attachments, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    email_data['email_id'],
                    email_data['subject'],
                    email_data['sender'],
                    email_data['received_at'],
                    email_data['body'],
                    json.dumps(email_data.get('attachments', [])),
                    'pending'
                ))
                conn.commit()
```

---

## 🔍 Verify Everything Works

Run the verification script:
```bash
python verify_system.py
```

This will check:
- ✅ Backend is running
- ✅ Frontend is accessible
- ✅ All API endpoints working
- ✅ Database tables exist
- ✅ Data is being returned

---

## 📊 Expected Results

After running the migration and adding sample data:

1. **Email Inbox Page** will show:
   - Total emails count
   - Processed emails count
   - List of emails with subjects, senders, and timestamps

2. **Email Stats** will display:
   - Total: 3
   - Processed: 2
   - Attachments: 2

3. **Email Details** will be clickable and show full email content

---

## 🎯 Next Steps

1. **Run Migration:** `python run_migration.py`
2. **Verify System:** `python verify_system.py`
3. **Add Sample Data:** Use the SQL above (optional)
4. **Refresh Browser:** F5 on Email Inbox page

Your Email Inbox will then be fully functional! 📬
