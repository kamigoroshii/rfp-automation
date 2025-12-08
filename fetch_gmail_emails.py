"""
Fetch Gmail Emails - All or Recent
Fetches emails from Gmail and saves to database
"""
from agents.sales.agent import SalesAgent
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def fetch_gmail_emails(days_back=30, max_emails=10):
    """
    Fetch emails from Gmail
    
    Args:
        days_back: Number of days to look back (default: 30)
        max_emails: Maximum number of emails to fetch (default: 10)
    """
    print("\n" + "="*60)
    print("  📧 FETCHING GMAIL EMAILS")
    print("="*60 + "\n")
    
    print(f"📅 Fetching emails from last {days_back} days")
    print(f"📊 Maximum: {max_emails} emails\n")
    
    print("🔍 Initializing Sales Agent...")
    agent = SalesAgent()
    
    print("📬 Connecting to Gmail IMAP...")
    print("⏳ This may take a few moments...\n")
    
    try:
        import imaplib
        import email
        from email.header import decode_header
        import os
        import uuid
        import json
        from orchestrator.config import settings
        
        # Connect to Gmail
        host = settings.EMAIL_HOST
        user = settings.EMAIL_USER
        password = settings.EMAIL_PASSWORD
        
        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        mail.select("inbox")
        
        # Calculate date for search
        since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
        
        # Search for emails from last N days
        print(f"🔎 Searching for emails since {since_date}...")
        status, messages = mail.search(None, f'(SINCE "{since_date}")')
        
        if status != "OK":
            print("❌ Failed to search emails")
            return
        
        email_ids = messages[0].split()
        total_found = len(email_ids)
        
        print(f"📧 Found {total_found} emails")
        
        # Limit to max_emails (get most recent)
        email_ids = email_ids[-max_emails:] if len(email_ids) > max_emails else email_ids
        
        print(f"📥 Fetching {len(email_ids)} most recent emails...\n")
        
        emails_saved = 0
        emails_skipped = 0
        
        for i, e_id in enumerate(email_ids, 1):
            try:
                # Fetch email
                res, msg_data = mail.fetch(e_id, "(RFC822)")
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        
                        sender = msg.get("From")
                        date_str = msg.get("Date")
                        
                        # Get body and attachments
                        body = ""
                        attachments = []
                        
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    try:
                                        body = part.get_payload(decode=True).decode()
                                    except:
                                        pass
                                
                                elif "attachment" in content_disposition:
                                    filename = part.get_filename()
                                    if filename and filename.lower().endswith(('.pdf', '.doc', '.docx')):
                                        # Save attachment
                                        save_dir = settings.UPLOAD_DIR
                                        os.makedirs(save_dir, exist_ok=True)
                                        
                                        file_id = str(uuid.uuid4())[:8]
                                        safe_filename = f"{file_id}_{filename}"
                                        filepath = os.path.join(save_dir, safe_filename)
                                        
                                        with open(filepath, "wb") as f:
                                            f.write(part.get_payload(decode=True))
                                        
                                        attachments.append(filepath)
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode()
                            except:
                                body = str(msg.get_payload())
                        
                        # Create email content
                        email_content = {
                            "subject": subject,
                            "sender": sender,
                            "body": body,
                            "attachments": attachments
                        }
                        
                        # Save to database
                        email_id = agent._save_email_to_db(email_content)
                        
                        print(f"  [{i}/{len(email_ids)}] ✅ {subject[:50]}...")
                        emails_saved += 1
                        
                        # Try to process as RFP
                        try:
                            rfp = agent.ingest_email_rfp(email_content, email_id)
                            if rfp:
                                agent._update_email_status(email_id, 'processed', rfp.rfp_id)
                                print(f"       🎯 Created RFP: {rfp.rfp_id}")
                        except:
                            pass  # Not all emails will be RFPs
                        
            except Exception as e:
                print(f"  [{i}/{len(email_ids)}] ⚠️  Error: {str(e)[:50]}...")
                emails_skipped += 1
                continue
        
        mail.close()
        mail.logout()
        
        print("\n" + "="*60)
        print(f"  ✅ COMPLETED!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"  • Emails saved: {emails_saved}")
        print(f"  • Emails skipped: {emails_skipped}")
        print(f"  • Total processed: {emails_saved + emails_skipped}")
        
        print("\n📬 Refresh your Email Inbox page to see the emails!")
        print("🌐 http://localhost:5173/emails")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check:")
        print("  1. Gmail credentials in .env file")
        print("  2. Run: python test_gmail_connection.py")

if __name__ == "__main__":
    import sys
    
    # Allow command line arguments
    days = 30
    max_emails = 10
    
    if len(sys.argv) > 1:
        days = int(sys.argv[1])
    if len(sys.argv) > 2:
        max_emails = int(sys.argv[2])
    
    fetch_gmail_emails(days_back=days, max_emails=max_emails)
