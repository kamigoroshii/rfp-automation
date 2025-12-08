"""
Check Gmail Now - Manual Trigger
Immediately fetches emails from Gmail instead of waiting for hourly check
"""
from agents.sales.agent import SalesAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def check_gmail_now():
    """Manually trigger Gmail check"""
    print("\n" + "="*60)
    print("  📧 CHECKING GMAIL FOR NEW RFPS")
    print("="*60 + "\n")
    
    print("🔍 Initializing Sales Agent...")
    agent = SalesAgent()
    
    print("📬 Connecting to Gmail IMAP...")
    print("⏳ This may take a few moments...\n")
    
    try:
        rfps = agent.check_emails_imap()
        
        print("\n" + "="*60)
        print(f"  ✅ FOUND {len(rfps)} NEW RFPs FROM GMAIL")
        print("="*60 + "\n")
        
        if rfps:
            print("📋 RFPs Created:")
            for rfp in rfps:
                print(f"  • {rfp.rfp_id}: {rfp.title}")
            
            print("\n📬 Emails have been saved to database!")
            print("🔄 Refresh your Email Inbox page to see them")
        else:
            print("ℹ️  No new unread emails found in Gmail")
            print("\nPossible reasons:")
            print("  • All emails are already read")
            print("  • No emails match RFP criteria")
            print("  • Inbox is empty")
            print("\nTip: Mark some emails as unread in Gmail and try again")
        
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check:")
        print("  1. Gmail credentials in .env file")
        print("  2. Run: python test_gmail_connection.py")
        print("  3. Check backend logs for details")

if __name__ == "__main__":
    check_gmail_now()
