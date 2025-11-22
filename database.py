"""
Database Management Module
Handles SQLite database initialization, connections, and CRUD operations
"""

import sqlite3
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
import os

class DatabaseManager:
    def __init__(self, db_name='hospital_management.db'):
        self.db_name = db_name
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        self.init_database()
    
    def _get_or_create_key(self):
        """Get or create encryption key for Fernet"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def get_connection(self):
        """Create and return database connection"""
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        """Initialize database with tables and default data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'doctor', 'receptionist')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                anonymized_name TEXT,
                anonymized_contact TEXT,
                encrypted_name TEXT,
                encrypted_contact TEXT,
                encrypted_diagnosis TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_anonymized INTEGER DEFAULT 0,
                data_retention_date TIMESTAMP,
                consent_given INTEGER DEFAULT 0
            )
        ''')
        
        # Create logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                role TEXT,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Create consent_records table (GDPR compliance)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consent_records (
                consent_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                consent_type TEXT,
                consent_given INTEGER DEFAULT 1,
                consent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        
        # Insert default users if not exists
        try:
            # Hash passwords for security
            admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
            doc_pass = hashlib.sha256('doc123'.encode()).hexdigest()
            rec_pass = hashlib.sha256('rec123'.encode()).hexdigest()
            
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, role) VALUES
                ('admin', ?, 'admin'),
                ('DrBob', ?, 'doctor'),
                ('Alice_recep', ?, 'receptionist')
            ''', (admin_pass, doc_pass, rec_pass))
            
            # Insert sample patients if table is empty
            cursor.execute('SELECT COUNT(*) FROM patients')
            if cursor.fetchone()[0] == 0:
                sample_patients = [
                    ('John Smith', '555-123-4567', 'Hypertension'),
                    ('Emma Johnson', '555-987-6543', 'Type 2 Diabetes'),
                    ('Michael Brown', '555-456-7890', 'Asthma'),
                    ('Sarah Davis', '555-321-0987', 'Migraine'),
                    ('David Wilson', '555-654-3210', 'Arthritis')
                ]
                for name, contact, diagnosis in sample_patients:
                    cursor.execute('''
                        INSERT INTO patients (name, contact, diagnosis, consent_given)
                        VALUES (?, ?, ?, 1)
                    ''', (name, contact, diagnosis))
            
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        
        conn.close()
    
    def authenticate_user(self, username, password):
        """Authenticate user and return user details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT user_id, username, role FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.log_action(user[0], username, user[2], 'login', f'User {username} logged in')
            return {'user_id': user[0], 'username': user[1], 'role': user[2]}
        return None
    
    def log_action(self, user_id, username, role, action, details=''):
        """Log user action for audit trail"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO logs (user_id, username, role, action, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, role, action, details))
        
        conn.commit()
        conn.close()
    
    def get_all_logs(self):
        """Retrieve all logs (Admin only)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT log_id, username, role, action, timestamp, details
            FROM logs
            ORDER BY timestamp DESC
        ''')
        
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    def get_logs_by_date_range(self, days=7):
        """Get logs for activity graphs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as count
            FROM logs
            WHERE timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (days,))
        
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    def get_action_counts(self, days=7):
        """Get action counts for graphs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action, COUNT(*) as count
            FROM logs
            WHERE timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY action
            ORDER BY count DESC
        ''', (days,))
        
        actions = cursor.fetchall()
        conn.close()
        return actions
    
    def encrypt_data(self, data):
        """Encrypt data using Fernet"""
        if data:
            return self.cipher.encrypt(data.encode()).decode()
        return None
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using Fernet"""
        if encrypted_data:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        return None
    
    def anonymize_patient_data(self, user_id, username, role):
        """Anonymize all patient records with Fernet encryption (reversible)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT patient_id, name, contact, diagnosis FROM patients WHERE is_anonymized = 0')
        patients = cursor.fetchall()
        
        anonymized_count = 0
        for patient in patients:
            patient_id, name, contact, diagnosis = patient
            
            # Create anonymized versions
            anon_name = f"ANON_{patient_id:04d}"
            anon_contact = "XXX-XXX-" + contact[-4:] if len(contact) >= 4 else "XXX-XXX-XXXX"
            
            # Encrypt original data (reversible with Fernet)
            encrypted_name = self.encrypt_data(name)
            encrypted_contact = self.encrypt_data(contact)
            encrypted_diagnosis = self.encrypt_data(diagnosis)
            
            cursor.execute('''
                UPDATE patients
                SET anonymized_name = ?,
                    anonymized_contact = ?,
                    encrypted_name = ?,
                    encrypted_contact = ?,
                    encrypted_diagnosis = ?,
                    is_anonymized = 1
                WHERE patient_id = ?
            ''', (anon_name, anon_contact, encrypted_name, encrypted_contact, 
                  encrypted_diagnosis, patient_id))
            
            anonymized_count += 1
        
        conn.commit()
        conn.close()
        
        self.log_action(user_id, username, role, 'anonymize_data', 
                       f'Anonymized {anonymized_count} patient records with Fernet encryption')
        
        return anonymized_count
    
    def de_anonymize_patient_data(self, user_id, username, role):
        """De-anonymize patient records (decrypt data)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, encrypted_name, encrypted_contact, encrypted_diagnosis 
            FROM patients WHERE is_anonymized = 1
        ''')
        patients = cursor.fetchall()
        
        de_anonymized_count = 0
        for patient in patients:
            patient_id, enc_name, enc_contact, enc_diagnosis = patient
            
            # Decrypt data
            if enc_name and enc_contact and enc_diagnosis:
                name = self.decrypt_data(enc_name)
                contact = self.decrypt_data(enc_contact)
                diagnosis = self.decrypt_data(enc_diagnosis)
                
                cursor.execute('''
                    UPDATE patients
                    SET name = ?,
                        contact = ?,
                        diagnosis = ?,
                        is_anonymized = 0
                    WHERE patient_id = ?
                ''', (name, contact, diagnosis, patient_id))
                
                de_anonymized_count += 1
        
        conn.commit()
        conn.close()
        
        self.log_action(user_id, username, role, 'de_anonymize_data', 
                       f'De-anonymized {de_anonymized_count} patient records')
        
        return de_anonymized_count
    
    def get_patients(self, role, show_anonymized=False):
        """Get patient data based on role"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if role == 'admin' and not show_anonymized:
            # Admin can see raw data
            cursor.execute('''
                SELECT patient_id, name, contact, diagnosis, date_added, 
                       is_anonymized, consent_given
                FROM patients
                ORDER BY patient_id DESC
            ''')
        elif role == 'admin' and show_anonymized:
            # Admin viewing anonymized data
            cursor.execute('''
                SELECT patient_id, 
                       CASE WHEN is_anonymized = 1 THEN anonymized_name ELSE name END as name,
                       CASE WHEN is_anonymized = 1 THEN anonymized_contact ELSE contact END as contact,
                       CASE WHEN is_anonymized = 1 THEN '[ENCRYPTED]' ELSE diagnosis END as diagnosis,
                       date_added, is_anonymized, consent_given
                FROM patients
                ORDER BY patient_id DESC
            ''')
        else:
            # Doctor and Receptionist see anonymized data only
            cursor.execute('''
                SELECT patient_id,
                       CASE WHEN is_anonymized = 1 THEN anonymized_name ELSE name END as name,
                       CASE WHEN is_anonymized = 1 THEN anonymized_contact ELSE contact END as contact,
                       CASE WHEN is_anonymized = 1 THEN '[ENCRYPTED]' ELSE diagnosis END as diagnosis,
                       date_added, is_anonymized, consent_given
                FROM patients
                ORDER BY patient_id DESC
            ''')
        
        patients = cursor.fetchall()
        conn.close()
        return patients
    
    def add_patient(self, name, contact, diagnosis, user_id, username, role, consent=True):
        """Add new patient record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Calculate data retention date (30 days from now as per GDPR)
            cursor.execute('''
                INSERT INTO patients (name, contact, diagnosis, consent_given, data_retention_date)
                VALUES (?, ?, ?, ?, datetime('now', '+30 days'))
            ''', (name, contact, diagnosis, 1 if consent else 0))
            
            patient_id = cursor.lastrowid
            
            # Record consent
            if consent:
                cursor.execute('''
                    INSERT INTO consent_records (patient_id, consent_type, consent_given)
                    VALUES (?, 'data_processing', 1)
                ''', (patient_id,))
            
            conn.commit()
            
            self.log_action(user_id, username, role, 'add_patient', 
                           f'Added new patient: {name}')
            
            conn.close()
            return True, "Patient added successfully"
        except Exception as e:
            conn.close()
            return False, f"Error adding patient: {str(e)}"
    
    def update_patient(self, patient_id, name, contact, diagnosis, user_id, username, role):
        """Update patient record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE patients
                SET name = ?, contact = ?, diagnosis = ?, is_anonymized = 0
                WHERE patient_id = ?
            ''', (name, contact, diagnosis, patient_id))
            
            conn.commit()
            
            self.log_action(user_id, username, role, 'update_patient', 
                           f'Updated patient ID: {patient_id}')
            
            conn.close()
            return True, "Patient updated successfully"
        except Exception as e:
            conn.close()
            return False, f"Error updating patient: {str(e)}"
    
    def delete_patient(self, patient_id, user_id, username, role):
        """Delete patient record (Admin only)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Delete associated consent records first
            cursor.execute('DELETE FROM consent_records WHERE patient_id = ?', (patient_id,))
            
            # Delete patient
            cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
            
            conn.commit()
            
            self.log_action(user_id, username, role, 'delete_patient', 
                           f'Deleted patient ID: {patient_id}')
            
            conn.close()
            return True, "Patient deleted successfully"
        except Exception as e:
            conn.close()
            return False, f"Error deleting patient: {str(e)}"
    
    def check_data_retention(self):
        """Check and delete records past retention date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT patient_id, name FROM patients
            WHERE data_retention_date < datetime('now')
        ''')
        
        expired_records = cursor.fetchall()
        
        for patient_id, name in expired_records:
            cursor.execute('DELETE FROM consent_records WHERE patient_id = ?', (patient_id,))
            cursor.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
            self.log_action(0, 'system', 'system', 'data_retention_cleanup', 
                           f'Auto-deleted expired patient record: {patient_id}')
        
        conn.commit()
        conn.close()
        
        return len(expired_records)
    
    def export_logs_csv(self):
        """Export logs to CSV format"""
        import csv
        import io
        
        logs = self.get_all_logs()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Log ID', 'Username', 'Role', 'Action', 'Timestamp', 'Details'])
        
        for log in logs:
            writer.writerow(log)
        
        return output.getvalue()
    
    def export_patients_csv(self, role):
        """Export patient data to CSV format"""
        import csv
        import io
        
        patients = self.get_patients(role)
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Patient ID', 'Name', 'Contact', 'Diagnosis', 'Date Added', 
                        'Is Anonymized', 'Consent Given'])
        
        for patient in patients:
            writer.writerow(patient)
        
        return output.getvalue()
