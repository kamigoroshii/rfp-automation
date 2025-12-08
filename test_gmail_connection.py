"""
Test Gmail Connection
Verifies that Gmail IMAP credentials are correct
"""
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

def test_gmail_connection():
    """Test Gmail IMAP connection"""
    host = os.getenv('EMAIL_HOST')
    user = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASSWORD')
    
    print("\n" + "="*60)
    print("  📧 TESTING GMAIL CONNECTION")
    print("="*60 + "\n")
    
    print(f"Host: {host}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
    
    if not host or not user or not password:
        print("\n❌ Email credentials not configured!")
        print("\nPlease update your .env file with:")
        print("  EMAIL_HOST=imap.gmail.com")
        print("  EMAIL_PORT=993")
        print("  EMAIL_USER=your-email@gmail.com")
        print("  EMAIL_PASSWORD=your-app-password")
        return False
    
    print(f"\n🔌 Connecting to {host}...")
    
    try:
        mail = imaplib.IMAP4_SSL(host)
        print("✅ SSL connection established")
        
        print(f"🔐 Logging in as {user}...")
        mail.login(user, password)
        print("✅ Login successful")
        
        print("📬 Selecting inbox...")
        mail.select("inbox")
        print("✅ Inbox selected")
        
        # Get email count
        status, messages = mail.search(None, "ALL")
        total_emails = len(messages[0].split()) if messages[0] else 0
        
        # Get unread count
        status, unread = mail.search(None, "UNSEEN")
        unread_count = len(unread[0].split()) if unread[0] else 0
        
        print(f"\n📊 Inbox Statistics:")
        print(f"  Total emails: {total_emails}")
        print(f"  Unread emails: {unread_count}")
        
        mail.close()
        mail.logout()
        
        print("\n🎉 SUCCESS! Gmail connection is working!")
        print("\nYour emails will be fetched automatically every hour.")
        print("Or run: python check_gmail_now.py to fetch immediately")
        
        return True
        
    except imaplib.IMAP4.error as e:
        print(f"\n❌ IMAP Error: {str(e)}")
        print("\nPossible issues:")
        print("  1. Wrong email or password")
        print("  2. Using regular password instead of App Password")
        print("  3. IMAP not enabled in Gmail settings")
        print("  4. 2-Step Verification not enabled")
        return False
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        print("\nPlease check:")
        print("  1. Internet connection")
        print("  2. Gmail credentials in .env file")
        print("  3. IMAP is enabled in Gmail")
        return False

if __name__ == "__main__":
    test_gmail_connection()
    print("\n" + "="*60 + "\n")
