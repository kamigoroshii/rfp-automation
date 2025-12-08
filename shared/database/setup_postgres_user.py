"""
Quick PostgreSQL User Setup
Alternative to SQL script - creates user programmatically
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
import sys

def create_postgres_user():
    """Create rfp_user in PostgreSQL"""
    
    print("=" * 60)
    print("PostgreSQL User Setup for RFP Automation System")
    print("=" * 60)
    print()
    
    # Get postgres superuser password
    print("Enter PostgreSQL superuser (postgres) password:")
    postgres_password = getpass.getpass()
    
    # Get desired password for rfp_user
    print("\nEnter password for new rfp_user:")
    rfp_password = getpass.getpass()
    print("Confirm password:")
    rfp_password_confirm = getpass.getpass()
    
    if rfp_password != rfp_password_confirm:
        print("❌ Passwords don't match!")
        return False
    
    try:
        # Connect as postgres superuser
        print("\n🔌 Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password=postgres_password,
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_user WHERE usename = 'rfp_user'"
        )
        exists = cursor.fetchone()
        
        if exists:
            print("⚠️  User 'rfp_user' already exists")
            print("Updating password...")
            cursor.execute(f"ALTER USER rfp_user WITH PASSWORD '{rfp_password}'")
            print("✅ Password updated successfully")
        else:
            print("👤 Creating user 'rfp_user'...")
            cursor.execute(f"CREATE USER rfp_user WITH PASSWORD '{rfp_password}'")
            print("✅ User created successfully")
        
        # Grant privileges
        print("🔐 Granting privileges...")
        cursor.execute("ALTER USER rfp_user CREATEDB")
        cursor.execute("GRANT CONNECT ON DATABASE postgres TO rfp_user")
        
        cursor.close()
        conn.close()
        
        print()
        print("=" * 60)
        print("🎉 Setup completed successfully!")
        print("=" * 60)
        print()
        print("📝 Next steps:")
        print("   1. Update your .env file with:")
        print("      DB_USER=rfp_user")
        print(f"      DB_PASSWORD={rfp_password}")
        print()
        print("   2. Run: python shared/database/init_db.py")
        print("=" * 60)
        
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ PostgreSQL Error: {e}")
        print("\nPossible issues:")
        print("  - Wrong postgres password")
        print("  - PostgreSQL not running")
        print("  - Connection settings incorrect")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = create_postgres_user()
    sys.exit(0 if success else 1)
