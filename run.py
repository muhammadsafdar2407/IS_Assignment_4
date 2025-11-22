"""
Quick Start Script for Hospital Management System
Run this to launch the application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        from cryptography.fernet import Fernet
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstalling dependencies...")
        return False

def install_dependencies():
    """Install required packages"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed successfully")

def run_application():
    """Run the Streamlit application"""
    print("\n" + "="*60)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM")
    print("="*60)
    print("\nStarting application...")
    print("Access at: http://localhost:8501")
    print("\nDefault Login Credentials:")
    print("  Admin: admin / admin123")
    print("  Doctor: DrBob / doc123")
    print("  Receptionist: Alice_recep / rec123")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    subprocess.run(["streamlit", "run", "app.py"])

def main():
    """Main execution"""
    print("🏥 Hospital Management System - Quick Start")
    print("="*60)
    
    # Check and install dependencies
    if not check_dependencies():
        install_dependencies()
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()
