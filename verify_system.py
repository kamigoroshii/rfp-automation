"""
System Verification Script
Checks if backend and frontend are working correctly
"""
import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_backend_health():
    """Check if backend is running"""
    print_header("BACKEND HEALTH CHECK")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Backend is not running or not accessible")
        print_info(f"Make sure backend is running on {BACKEND_URL}")
        return False
    except Exception as e:
        print_error(f"Error checking backend: {str(e)}")
        return False

def check_frontend():
    """Check if frontend is accessible"""
    print_header("FRONTEND HEALTH CHECK")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print_success("Frontend is running")
            return True
        else:
            print_error(f"Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Frontend is not running or not accessible")
        print_info(f"Make sure frontend is running on {FRONTEND_URL}")
        return False
    except Exception as e:
        print_error(f"Error checking frontend: {str(e)}")
        return False

def check_api_endpoints():
    """Check critical API endpoints"""
    print_header("API ENDPOINTS CHECK")
    
    endpoints = [
        ("/api/rfp/list", "RFP List"),
        ("/api/analytics/dashboard", "Analytics Dashboard"),
        ("/api/products/search?query=", "Product Search"),
        ("/api/emails/list", "Email List"),
        ("/api/auditor/reports", "Auditor Reports"),
    ]
    
    results = []
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print_success(f"{name}: OK")
                data = response.json()
                
                # Show data counts
                if 'rfps' in data:
                    print_info(f"  → {len(data['rfps'])} RFPs found")
                elif 'products' in data:
                    print_info(f"  → {len(data['products'])} products found")
                elif 'emails' in data:
                    print_info(f"  → {len(data['emails'])} emails found")
                elif 'reports' in data:
                    print_info(f"  → {len(data['reports'])} reports found")
                
                results.append((name, True, None))
            else:
                print_error(f"{name}: Failed (Status {response.status_code})")
                results.append((name, False, f"Status {response.status_code}"))
        except Exception as e:
            print_error(f"{name}: Error - {str(e)}")
            results.append((name, False, str(e)))
    
    return results

def check_database_tables():
    """Check if required database tables exist"""
    print_header("DATABASE TABLES CHECK")
    
    try:
        # Check via API if we can get data
        response = requests.get(f"{BACKEND_URL}/api/rfp/list", timeout=5)
        if response.status_code == 200:
            print_success("Database connection working (rfps table accessible)")
        
        # Check emails table
        response = requests.get(f"{BACKEND_URL}/api/emails/list", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'emails' in data:
                print_success(f"Emails table exists ({len(data['emails'])} records)")
            else:
                print_warning("Emails table exists but is empty")
        else:
            print_error("Emails table might not exist or is inaccessible")
            print_info("Run: python run_migration.py")
        
        # Check audit_reports table
        response = requests.get(f"{BACKEND_URL}/api/auditor/reports", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'reports' in data:
                print_success(f"Audit reports table exists ({len(data['reports'])} records)")
            else:
                print_warning("Audit reports table exists but is empty")
        else:
            print_error("Audit reports table might not exist")
            print_info("Run: python run_migration.py")
            
    except Exception as e:
        print_error(f"Error checking database: {str(e)}")

def generate_report(backend_ok, frontend_ok, api_results):
    """Generate final report"""
    print_header("VERIFICATION REPORT")
    
    total_checks = len(api_results) + 2  # APIs + backend + frontend
    passed_checks = sum([1 for _, status, _ in api_results if status])
    if backend_ok:
        passed_checks += 1
    if frontend_ok:
        passed_checks += 1
    
    print(f"\n📊 Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print_success("All systems operational! 🎉")
    elif passed_checks >= total_checks * 0.7:
        print_warning("Most systems working, some issues detected")
    else:
        print_error("Multiple system failures detected")
    
    # Recommendations
    print("\n📝 Recommendations:")
    
    if not backend_ok:
        print("  1. Start the backend: uvicorn orchestrator.api.main:app --reload --port 8000")
    
    if not frontend_ok:
        print("  2. Start the frontend: cd frontend && npm run dev")
    
    # Check for empty emails
    for name, status, error in api_results:
        if name == "Email List" and status:
            print("  3. Email inbox is empty - run database migration and configure email agent")
            print("     → python run_migration.py")
            break
    
    print("\n" + "="*60)
    print(f"Verification completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

def main():
    print("\n" + "🔍 RFP AUTOMATION SYSTEM VERIFICATION".center(60))
    print("="*60)
    
    # Run checks
    backend_ok = check_backend_health()
    frontend_ok = check_frontend()
    api_results = check_api_endpoints()
    check_database_tables()
    
    # Generate report
    generate_report(backend_ok, frontend_ok, api_results)

if __name__ == "__main__":
    main()
