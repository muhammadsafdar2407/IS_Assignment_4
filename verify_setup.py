"""
Project Setup Verification Script
Checks that everything is ready for demonstration
"""

import os
import sys

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_files():
    """Verify all required files exist"""
    print_header("📁 FILE STRUCTURE CHECK")
    
    required_files = {
        'app.py': 'Main Streamlit application',
        'database.py': 'Database management module',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Complete documentation',
        'Assignment4.ipynb': 'Code documentation notebook',
        'QUICKSTART.md': 'Quick start guide',
        'CONFIG.md': 'Configuration guide',
        'FEATURES.md': 'Feature matrix',
        'run.py': 'Launch script',
        'test_system.py': 'Test suite'
    }
    
    all_present = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename:25} ({size:,} bytes) - {description}")
        else:
            print(f"  ❌ {filename:25} MISSING - {description}")
            all_present = False
    
    return all_present

def check_dependencies():
    """Check if dependencies are installed"""
    print_header("📦 DEPENDENCY CHECK")
    
    dependencies = {
        'streamlit': 'Web framework',
        'pandas': 'Data manipulation',
        'plotly': 'Visualization',
        'cryptography': 'Encryption'
    }
    
    all_installed = True
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"  ✅ {package:20} installed - {description}")
        except ImportError:
            print(f"  ❌ {package:20} MISSING - {description}")
            all_installed = False
    
    return all_installed

def check_code_quality():
    """Verify code files can be imported"""
    print_header("🔍 CODE QUALITY CHECK")
    
    try:
        import database
        print("  ✅ database.py - Imports successfully")
        
        # Check key functions exist
        if hasattr(database, 'DatabaseManager'):
            print("  ✅ DatabaseManager class - Found")
        else:
            print("  ❌ DatabaseManager class - Not found")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Error importing database.py: {e}")
        return False

def show_project_stats():
    """Display project statistics"""
    print_header("📊 PROJECT STATISTICS")
    
    # Count lines of code
    files_to_count = ['app.py', 'database.py', 'run.py', 'test_system.py']
    total_lines = 0
    
    for filename in files_to_count:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"  📄 {filename:20} {lines:5} lines")
    
    print(f"\n  📈 Total Code Lines: {total_lines:,}")
    
    # Count documentation
    doc_files = ['README.md', 'QUICKSTART.md', 'CONFIG.md', 'FEATURES.md']
    doc_chars = 0
    
    print(f"\n  📚 Documentation Files:")
    for filename in doc_files:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                chars = len(f.read())
                doc_chars += chars
                print(f"  📝 {filename:20} {chars:7,} chars")
    
    print(f"\n  📖 Total Documentation: {doc_chars:,} characters")

def show_features():
    """Display implemented features"""
    print_header("✨ IMPLEMENTED FEATURES")
    
    features = {
        "Confidentiality": [
            "SHA-256 Password Hashing",
            "Fernet Encryption (Reversible)",
            "Data Masking (ANON_XXXX)",
            "Role-Based Access Control",
            "Secure Authentication"
        ],
        "Integrity": [
            "Complete Audit Logging",
            "Timestamp All Actions",
            "Data Validation",
            "Database Constraints",
            "Log Export (CSV)"
        ],
        "Availability": [
            "Error Handling",
            "Data Backup (CSV)",
            "Stable Database",
            "System Monitoring",
            "Recovery Options"
        ],
        "Bonus Features": [
            "Fernet Encryption",
            "Real-time Activity Graphs",
            "Data Retention Timer",
            "Consent Banner",
            "GDPR Compliance Tools"
        ]
    }
    
    for category, items in features.items():
        print(f"\n  🎯 {category}:")
        for item in items:
            print(f"    ✅ {item}")

def show_credentials():
    """Display login credentials"""
    print_header("🔑 LOGIN CREDENTIALS")
    
    print("\n  Role: Admin")
    print("    Username: admin")
    print("    Password: admin123")
    print("    Access: Full system control")
    
    print("\n  Role: Doctor")
    print("    Username: DrBob")
    print("    Password: doc123")
    print("    Access: View anonymized data only")
    
    print("\n  Role: Receptionist")
    print("    Username: Alice_recep")
    print("    Password: rec123")
    print("    Access: Add/edit patient records")

def show_commands():
    """Display useful commands"""
    print_header("🚀 QUICK COMMANDS")
    
    print("\n  Install Dependencies:")
    print("    pip install -r requirements.txt")
    
    print("\n  Run Tests:")
    print("    python test_system.py")
    
    print("\n  Start Application (Option 1):")
    print("    python run.py")
    
    print("\n  Start Application (Option 2):")
    print("    streamlit run app.py")
    
    print("\n  Access Application:")
    print("    http://localhost:8501")
    
    print("\n  Change Port:")
    print("    streamlit run app.py --server.port 8502")

def generate_submission_checklist():
    """Generate submission checklist"""
    print_header("📋 SUBMISSION CHECKLIST")
    
    checklist = [
        ("Source Code Files", True, ".py files"),
        ("Database Schema", True, "Implemented in database.py"),
        ("Requirements File", True, "requirements.txt"),
        ("Jupyter Notebook", True, "Assignment4.ipynb with comments"),
        ("README Documentation", True, "Complete guide"),
        ("PDF Report", False, "3-5 pages with screenshots"),
        ("Demo Video", False, "Optional, 2-3 mins with drive link")
    ]
    
    print("\n  Ready for submission:")
    for item, done, note in checklist:
        status = "✅" if done else "⏳"
        print(f"  {status} {item:25} - {note}")

def main():
    """Main verification process"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🏥 HOSPITAL MANAGEMENT SYSTEM - SETUP VERIFICATION  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run checks
    files_ok = check_files()
    deps_ok = check_dependencies()
    code_ok = check_code_quality()
    
    # Show information
    show_project_stats()
    show_features()
    show_credentials()
    show_commands()
    generate_submission_checklist()
    
    # Final summary
    print_header("🎯 VERIFICATION SUMMARY")
    
    checks = {
        "File Structure": files_ok,
        "Dependencies": deps_ok,
        "Code Quality": code_ok
    }
    
    all_passed = all(checks.values())
    
    for check, status in checks.items():
        result = "✅ PASSED" if status else "❌ FAILED"
        print(f"  {check:20} {result}")
    
    print("\n" + "="*60)
    
    if all_passed:
        print("\n  🎉 SYSTEM READY FOR DEMONSTRATION!")
        print("  All checks passed. You can now:")
        print("    1. Run 'python run.py' to start")
        print("    2. Access http://localhost:8501")
        print("    3. Login and test features")
        print("    4. Prepare PDF report and demo video")
    else:
        print("\n  ⚠️ SETUP INCOMPLETE")
        print("  Please fix the failed checks above.")
        if not deps_ok:
            print("  Run: pip install -r requirements.txt")
    
    print("\n" + "="*60)
    print()
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
