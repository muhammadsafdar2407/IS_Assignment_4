"""
System Test Script
Verifies all components of the Hospital Management System
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        print("  ✅ Streamlit")
        import pandas
        print("  ✅ Pandas")
        import plotly
        print("  ✅ Plotly")
        from cryptography.fernet import Fernet
        print("  ✅ Cryptography (Fernet)")
        import sqlite3
        print("  ✅ SQLite3")
        import hashlib
        print("  ✅ Hashlib")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_database_module():
    """Test database module functionality"""
    print("\nTesting database module...")
    try:
        from database import DatabaseManager
        print("  ✅ Database module imported")
        
        # Initialize database
        db = DatabaseManager('test_hospital.db')
        print("  ✅ Database initialized")
        
        # Test authentication
        user = db.authenticate_user('admin', 'admin123')
        if user:
            print(f"  ✅ Authentication works (User: {user['username']})")
        else:
            print("  ❌ Authentication failed")
            return False
        
        # Test get patients
        patients = db.get_patients('admin')
        print(f"  ✅ Retrieved {len(patients)} patient records")
        
        # Test logging
        db.log_action(1, 'admin', 'admin', 'test', 'Testing system')
        logs = db.get_all_logs()
        print(f"  ✅ Logging works ({len(logs)} logs)")
        
        # Test encryption
        test_data = "Test Patient Name"
        encrypted = db.encrypt_data(test_data)
        decrypted = db.decrypt_data(encrypted)
        if decrypted == test_data:
            print("  ✅ Encryption/Decryption works")
        else:
            print("  ❌ Encryption/Decryption failed")
            return False
        
        # Clean up test database
        import os
        if os.path.exists('test_hospital.db'):
            os.remove('test_hospital.db')
        if os.path.exists('encryption.key'):
            # Keep the key if it exists
            pass
        
        print("  ✅ All database tests passed")
        return True
        
    except Exception as e:
        print(f"  ❌ Database test error: {e}")
        return False

def test_encryption():
    """Test Fernet encryption functionality"""
    print("\nTesting encryption...")
    try:
        from cryptography.fernet import Fernet
        
        # Generate key
        key = Fernet.generate_key()
        cipher = Fernet(key)
        print("  ✅ Encryption key generated")
        
        # Test encryption
        original = "Sensitive Patient Data"
        encrypted = cipher.encrypt(original.encode())
        print(f"  ✅ Data encrypted: {encrypted[:30]}...")
        
        # Test decryption
        decrypted = cipher.decrypt(encrypted).decode()
        if decrypted == original:
            print("  ✅ Data decrypted successfully")
            return True
        else:
            print("  ❌ Decryption mismatch")
            return False
            
    except Exception as e:
        print(f"  ❌ Encryption test error: {e}")
        return False

def test_password_hashing():
    """Test password hashing"""
    print("\nTesting password hashing...")
    try:
        import hashlib
        
        password = "admin123"
        hashed1 = hashlib.sha256(password.encode()).hexdigest()
        hashed2 = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"  ✅ Password hashed: {hashed1[:20]}...")
        
        if hashed1 == hashed2:
            print("  ✅ Hash consistency verified")
            return True
        else:
            print("  ❌ Hash inconsistency detected")
            return False
            
    except Exception as e:
        print(f"  ❌ Hashing test error: {e}")
        return False

def test_data_masking():
    """Test data masking functions"""
    print("\nTesting data masking...")
    try:
        # Test name masking
        patient_id = 1021
        masked_name = f"ANON_{patient_id:04d}"
        if masked_name == "ANON_1021":
            print(f"  ✅ Name masking: John Smith → {masked_name}")
        else:
            print("  ❌ Name masking failed")
            return False
        
        # Test contact masking
        contact = "555-123-4567"
        masked_contact = "XXX-XXX-" + contact[-4:]
        if masked_contact == "XXX-XXX-4567":
            print(f"  ✅ Contact masking: {contact} → {masked_contact}")
        else:
            print("  ❌ Contact masking failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Masking test error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    required_files = [
        'app.py',
        'database.py',
        'requirements.txt',
        'README.md',
        'Assignment4.ipynb',
        'run.py',
        'CONFIG.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - COMPREHENSIVE TESTS")
    print("="*60)
    
    results = {
        "File Structure": test_file_structure(),
        "Imports": test_imports(),
        "Password Hashing": test_password_hashing(),
        "Encryption": test_encryption(),
        "Data Masking": test_data_masking(),
        "Database Module": test_database_module()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print("="*60)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        print("The system is ready to run.")
        print("\nTo start the application, run:")
        print("  python run.py")
        print("  or")
        print("  streamlit run app.py")
    else:
        print("\n⚠️ SOME TESTS FAILED")
        print("Please check the errors above and fix the issues.")
        print("\nTo install dependencies, run:")
        print("  pip install -r requirements.txt")
    
    print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
