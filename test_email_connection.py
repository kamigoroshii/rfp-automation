import sys
import os
import imaplib
import logging

# Add the current directory to sys.path to allow importing orchestrator
sys.path.append(os.getcwd())

try:
    from orchestrator.config import settings
except ImportError:
    print("Error: Could not import orchestrator.config. Make sure you are running this from the project root.")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmailCheck")

def check_email_connection():
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    user = settings.EMAIL_USER
    password = settings.EMAIL_PASSWORD

    print(f"Checking email configuration:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  User: {user}")
    print(f"  Password: {'*' * len(password) if password else '[EMPTY]'}")

    if not host or not user or not password:
        print("\nERROR: Missing email configuration values.")
        return False

    try:
        print(f"\nAttempting to connect to {host}:{port}...")
        mail = imaplib.IMAP4_SSL(host, port)
        print("Connection established. Attempting login...")
        
        mail.login(user, password)
        print("\nSUCCESS: Login successful!")
        
        mail.logout()
        return True
    except imaplib.IMAP4.error as e:
        print(f"\nLOGIN FAILED: {e}")
        print("Note: If you are using Gmail, make sure you are using an App Password, not your regular login password.")
        print("      Also assure 'Less secure app access' is not the issue (App Passwords bypass this).")
        return False
    except Exception as e:
        print(f"\nERROR: An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    check_email_connection()
