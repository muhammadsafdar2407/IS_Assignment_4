"""
GDPR-Compliant Hospital Management System
Main Streamlit Application
Implements CIA Triad: Confidentiality, Integrity, Availability
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager
import time

# Page configuration
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for elegant UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .header-title {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.9rem;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_db():
    return DatabaseManager()

db = init_db()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.consent_shown = False

def show_consent_banner():
    """GDPR Consent Banner"""
    if not st.session_state.consent_shown:
        with st.container():
            st.markdown("""
                <div class="info-box">
                    <h4>🔒 GDPR Data Privacy Notice</h4>
                    <p>This system processes personal health data in compliance with GDPR. We collect and process data solely for healthcare purposes. 
                    You have the right to access, rectify, or delete your data. Data retention period: 30 days unless required longer for medical records.</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                if st.button("✅ I Understand", key="consent_accept"):
                    st.session_state.consent_shown = True
                    st.rerun()
            with col3:
                if st.button("📋 Privacy Policy", key="consent_policy"):
                    st.info("**Privacy Policy**: Your data is encrypted, anonymized, and protected according to GDPR standards. All access is logged for audit purposes.")

def login_page():
    """Login Page with Authentication"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='header-title' style='text-align: center;'>🏥 Hospital Management</h1>", unsafe_allow_html=True)
        st.markdown("<p class='header-subtitle' style='text-align: center;'>GDPR-Compliant Patient Data System</p>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
                <div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <h3 style='text-align: center; color: #2c3e50; margin-bottom: 1.5rem;'>🔐 Secure Login</h3>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if username and password:
                        try:
                            user = db.authenticate_user(username, password)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.user = user
                                st.success(f"✅ Welcome, {user['username']}! Role: {user['role'].upper()}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Invalid credentials. Please try again.")
                        except Exception as e:
                            st.error(f"🚨 Login error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter both username and password.")
        
        # Default credentials info
        with st.expander("ℹ️ Default Login Credentials"):
            st.markdown("""
            **Admin:**
            - Username: `admin`
            - Password: `admin123`
            
            **Doctor:**
            - Username: `DrBob`
            - Password: `doc123`
            
            **Receptionist:**
            - Username: `Alice_recep`
            - Password: `rec123`
            """)

def admin_dashboard():
    """Admin Dashboard - Full Access"""
    user = st.session_state.user
    
    st.markdown(f"<h1 class='header-title'>👨‍💼 Admin Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='header-subtitle'>Welcome, {user['username']} | Full System Access</p>", unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "👥 Patient Management", "🔒 Data Security", 
        "📋 Audit Logs", "📈 Analytics", "⚙️ GDPR Compliance"
    ])
    
    with tab1:
        show_overview_dashboard()
    
    with tab2:
        show_patient_management(user, is_admin=True)
    
    with tab3:
        show_data_security(user)
    
    with tab4:
        show_audit_logs(user)
    
    with tab5:
        show_analytics()
    
    with tab6:
        show_gdpr_compliance(user)

def doctor_dashboard():
    """Doctor Dashboard - Anonymized Data Access"""
    user = st.session_state.user
    
    st.markdown(f"<h1 class='header-title'>👨‍⚕️ Doctor Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='header-subtitle'>Welcome, Dr. {user['username']} | Anonymized Patient Data View</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 Overview", "👥 View Patients"])
    
    with tab1:
        show_overview_dashboard()
    
    with tab2:
        show_patient_list(user, can_edit=False)

def receptionist_dashboard():
    """Receptionist Dashboard - Add/Edit Records"""
    user = st.session_state.user
    
    st.markdown(f"<h1 class='header-title'>👩‍💼 Receptionist Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='header-subtitle'>Welcome, {user['username']} | Patient Records Management</p>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "➕ Add Patient", "✏️ Edit Patient"])
    
    with tab1:
        show_overview_dashboard()
    
    with tab2:
        add_patient_form(user)
    
    with tab3:
        edit_patient_form(user)

def show_overview_dashboard():
    """Overview metrics for all roles"""
    try:
        patients = db.get_patients(st.session_state.user['role'])
        logs = db.get_all_logs()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class='metric-card'>
                    <h3 style='color: #3498db;'>👥 Total Patients</h3>
                    <p style='font-size: 2.5rem; font-weight: 700; color: #2c3e50;'>{}</p>
                </div>
            """.format(len(patients)), unsafe_allow_html=True)
        
        with col2:
            anonymized = sum(1 for p in patients if p[5] == 1)
            st.markdown("""
                <div class='metric-card'>
                    <h3 style='color: #e74c3c;'>🔒 Anonymized</h3>
                    <p style='font-size: 2.5rem; font-weight: 700; color: #2c3e50;'>{}</p>
                </div>
            """.format(anonymized), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class='metric-card'>
                    <h3 style='color: #2ecc71;'>✅ With Consent</h3>
                    <p style='font-size: 2.5rem; font-weight: 700; color: #2c3e50;'>{}</p>
                </div>
            """.format(sum(1 for p in patients if p[6] == 1)), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class='metric-card'>
                    <h3 style='color: #f39c12;'>📋 Total Logs</h3>
                    <p style='font-size: 2.5rem; font-weight: 700; color: #2c3e50;'>{}</p>
                </div>
            """.format(len(logs)), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recent activity
        st.subheader("📊 Recent System Activity")
        if logs:
            recent_logs = logs[:10]
            df_logs = pd.DataFrame(recent_logs, columns=['Log ID', 'Username', 'Role', 'Action', 'Timestamp', 'Details'])
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
        else:
            st.info("No recent activity recorded.")
            
    except Exception as e:
        st.error(f"🚨 Error loading overview: {str(e)}")

def show_patient_management(user, is_admin=False):
    """Patient management for admin"""
    st.subheader("👥 Patient Data Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        view_mode = st.radio(
            "Select View Mode:",
            ["Raw Data (Admin Only)", "Anonymized View"],
            horizontal=True
        )
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    show_anonymized = view_mode == "Anonymized View"
    patients = db.get_patients(user['role'], show_anonymized=show_anonymized)
    
    if patients:
        df = pd.DataFrame(patients, columns=['ID', 'Name', 'Contact', 'Diagnosis', 'Date Added', 'Anonymized', 'Consent'])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export option
        csv_data = db.export_patients_csv(user['role'])
        st.download_button(
            label="📥 Download Patient Data (CSV)",
            data=csv_data,
            file_name=f"patients_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Delete patient (Admin only)
        if is_admin:
            st.markdown("---")
            st.subheader("🗑️ Delete Patient Record")
            col_a, col_b = st.columns([3, 1])
            with col_a:
                patient_id_to_delete = st.number_input("Enter Patient ID to Delete", min_value=1, step=1, key="delete_id")
            with col_b:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Delete", type="primary", use_container_width=True):
                    success, message = db.delete_patient(patient_id_to_delete, user['user_id'], user['username'], user['role'])
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
    else:
        st.info("No patient records found.")

def show_patient_list(user, can_edit=False):
    """Display patient list for doctors"""
    st.subheader("👥 Patient Records (Anonymized)")
    
    patients = db.get_patients(user['role'])
    
    if patients:
        df = pd.DataFrame(patients, columns=['ID', 'Name', 'Contact', 'Diagnosis', 'Date Added', 'Anonymized', 'Consent'])
        
        # Apply styling
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.info("ℹ️ Patient data is displayed in anonymized format to protect privacy.")
        
        # Log view action
        db.log_action(user['user_id'], user['username'], user['role'], 
                     'view_patients', f'Viewed {len(patients)} patient records')
    else:
        st.warning("⚠️ No patient records available.")

def add_patient_form(user):
    """Form to add new patient"""
    st.subheader("➕ Add New Patient Record")
    
    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Patient Name*", placeholder="Enter full name")
            contact = st.text_input("📞 Contact Number*", placeholder="555-123-4567")
        
        with col2:
            diagnosis = st.text_input("🏥 Diagnosis*", placeholder="Enter diagnosis")
            consent = st.checkbox("✅ Patient Consent Given", value=True)
        
        st.markdown("---")
        submit = st.form_submit_button("💾 Add Patient Record", use_container_width=True, type="primary")
        
        if submit:
            if name and contact and diagnosis:
                success, message = db.add_patient(name, contact, diagnosis, 
                                                 user['user_id'], user['username'], 
                                                 user['role'], consent)
                if success:
                    st.success(f"✅ {message}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.warning("⚠️ Please fill in all required fields.")

def edit_patient_form(user):
    """Form to edit existing patient"""
    st.subheader("✏️ Edit Patient Record")
    
    patients = db.get_patients('admin', show_anonymized=False)
    
    if patients:
        # Select patient
        patient_options = {f"ID: {p[0]} - {p[1]}": p[0] for p in patients}
        selected = st.selectbox("Select Patient to Edit", list(patient_options.keys()))
        patient_id = patient_options[selected]
        
        # Get current data
        current_patient = [p for p in patients if p[0] == patient_id][0]
        
        with st.form("edit_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("👤 Patient Name", value=current_patient[1])
                contact = st.text_input("📞 Contact Number", value=current_patient[2])
            
            with col2:
                diagnosis = st.text_input("🏥 Diagnosis", value=current_patient[3])
            
            st.markdown("---")
            submit = st.form_submit_button("💾 Update Patient Record", use_container_width=True, type="primary")
            
            if submit:
                if name and contact and diagnosis:
                    success, message = db.update_patient(patient_id, name, contact, diagnosis,
                                                        user['user_id'], user['username'], user['role'])
                    if success:
                        st.success(f"✅ {message}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ All fields are required.")
    else:
        st.info("No patient records available for editing.")

def show_data_security(user):
    """Data security controls for admin"""
    st.subheader("🔒 Data Security & Anonymization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='info-box'>
                <h4>🔐 Fernet Encryption (Reversible)</h4>
                <p>Patient data is encrypted using Fernet symmetric encryption. 
                This allows for reversible anonymization while maintaining data security.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔒 Anonymize All Patient Data", use_container_width=True, type="primary"):
            with st.spinner("Encrypting patient data..."):
                count = db.anonymize_patient_data(user['user_id'], user['username'], user['role'])
                st.success(f"✅ Successfully anonymized {count} patient records with Fernet encryption!")
                time.sleep(1)
                st.rerun()
    
    with col2:
        st.markdown("""
            <div class='warning-box'>
                <h4>🔓 De-Anonymization (Admin Only)</h4>
                <p>Decrypt and restore original patient data. This action requires admin privileges 
                and will be logged in the audit trail.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔓 De-Anonymize Patient Data", use_container_width=True):
            with st.spinner("Decrypting patient data..."):
                count = db.de_anonymize_patient_data(user['user_id'], user['username'], user['role'])
                st.success(f"✅ Successfully de-anonymized {count} patient records!")
                time.sleep(1)
                st.rerun()
    
    st.markdown("---")
    
    # Encryption status
    patients = db.get_patients(user['role'])
    anonymized_count = sum(1 for p in patients if p[5] == 1)
    total_count = len(patients)
    
    st.subheader("📊 Encryption Status")
    
    if total_count > 0:
        progress = anonymized_count / total_count
        st.progress(progress)
        st.metric("Anonymized Records", f"{anonymized_count} / {total_count}", 
                 f"{progress*100:.1f}% encrypted")
    else:
        st.info("No patient records in database.")

def show_audit_logs(user):
    """Display audit logs for integrity monitoring"""
    st.subheader("📋 Integrity Audit Logs")
    
    st.markdown("""
        <div class='info-box'>
            <h4>🔍 Audit Trail System</h4>
            <p>All user actions are logged with timestamps for complete accountability and GDPR compliance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    logs = db.get_all_logs()
    
    if logs:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        df_logs = pd.DataFrame(logs, columns=['Log ID', 'Username', 'Role', 'Action', 'Timestamp', 'Details'])
        
        with col1:
            filter_role = st.multiselect("Filter by Role", df_logs['Role'].unique(), default=df_logs['Role'].unique())
        
        with col2:
            filter_action = st.multiselect("Filter by Action", df_logs['Action'].unique(), default=df_logs['Action'].unique())
        
        with col3:
            limit = st.selectbox("Show Records", [10, 25, 50, 100, "All"], index=0)
        
        # Apply filters
        filtered_df = df_logs[
            (df_logs['Role'].isin(filter_role)) &
            (df_logs['Action'].isin(filter_action))
        ]
        
        if limit != "All":
            filtered_df = filtered_df.head(limit)
        
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        # Export logs
        csv_data = db.export_logs_csv()
        st.download_button(
            label="📥 Download Audit Logs (CSV)",
            data=csv_data,
            file_name=f"audit_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Log statistics
        st.markdown("---")
        st.subheader("📊 Log Statistics")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Total Log Entries", len(df_logs))
        
        with col_b:
            unique_users = df_logs['Username'].nunique()
            st.metric("Unique Users", unique_users)
        
        with col_c:
            unique_actions = df_logs['Action'].nunique()
            st.metric("Action Types", unique_actions)
        
    else:
        st.info("No audit logs available yet.")

def show_analytics():
    """Show analytics and activity graphs (Bonus Feature)"""
    st.subheader("📈 Real-Time Activity Analytics")
    
    # Time range selector
    col1, col2 = st.columns([3, 1])
    with col1:
        days = st.slider("Select Time Range (days)", 1, 30, 7)
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get data
    daily_logs = db.get_logs_by_date_range(days)
    action_counts = db.get_action_counts(days)
    
    if daily_logs or action_counts:
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Daily activity chart
            if daily_logs:
                df_daily = pd.DataFrame(daily_logs, columns=['Date', 'Count'])
                fig_daily = px.line(df_daily, x='Date', y='Count', 
                                   title=f'Daily Activity (Last {days} days)',
                                   markers=True)
                fig_daily.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Number of Actions",
                    hovermode='x unified'
                )
                st.plotly_chart(fig_daily, use_container_width=True)
            else:
                st.info("No daily activity data available.")
        
        with col_b:
            # Action distribution chart
            if action_counts:
                df_actions = pd.DataFrame(action_counts, columns=['Action', 'Count'])
                fig_actions = px.pie(df_actions, names='Action', values='Count',
                                    title=f'Action Distribution (Last {days} days)',
                                    hole=0.4)
                st.plotly_chart(fig_actions, use_container_width=True)
            else:
                st.info("No action data available.")
        
        # Action breakdown table
        st.markdown("---")
        st.subheader("📊 Action Breakdown")
        if action_counts:
            df_actions = pd.DataFrame(action_counts, columns=['Action Type', 'Count'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(df_actions, use_container_width=True, hide_index=True)
            
            with col2:
                # Top actions
                st.markdown("**Top 3 Actions:**")
                for i, (action, count) in enumerate(action_counts[:3], 1):
                    st.markdown(f"{i}. **{action}**: {count} times")
    else:
        st.info(f"No activity data available for the last {days} days.")

def show_gdpr_compliance(user):
    """GDPR compliance features (Bonus)"""
    st.subheader("⚙️ GDPR Compliance Tools")
    
    # Data Retention Management
    st.markdown("### 📅 Data Retention Management")
    st.markdown("""
        <div class='info-box'>
            <p>Patient records are automatically retained for 30 days from creation. 
            Records past the retention date will be automatically removed.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Run Data Retention Cleanup", use_container_width=True, type="primary"):
            with st.spinner("Checking for expired records..."):
                expired_count = db.check_data_retention()
                if expired_count > 0:
                    st.success(f"✅ Removed {expired_count} expired patient record(s)")
                    db.log_action(user['user_id'], user['username'], user['role'], 
                                 'manual_retention_cleanup', 
                                 f'Manually triggered retention cleanup, removed {expired_count} records')
                else:
                    st.info("✅ No expired records found.")
    
    with col2:
        # Show retention statistics
        patients = db.get_patients(user['role'])
        st.metric("Total Active Records", len(patients))
        st.info("Retention period: 30 days")
    
    st.markdown("---")
    
    # Consent Management
    st.markdown("### ✅ Consent Management")
    patients = db.get_patients(user['role'])
    
    if patients:
        consent_given = sum(1 for p in patients if p[6] == 1)
        consent_rate = (consent_given / len(patients)) * 100 if patients else 0
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("Patients with Consent", f"{consent_given} / {len(patients)}")
        
        with col_b:
            st.metric("Consent Rate", f"{consent_rate:.1f}%")
        
        # Consent pie chart
        fig_consent = go.Figure(data=[go.Pie(
            labels=['Consent Given', 'No Consent'],
            values=[consent_given, len(patients) - consent_given],
            hole=.3,
            marker_colors=['#2ecc71', '#e74c3c']
        )])
        fig_consent.update_layout(title="Consent Status Distribution")
        st.plotly_chart(fig_consent, use_container_width=True)
    else:
        st.info("No patient records available.")
    
    st.markdown("---")
    
    # GDPR Rights Summary
    st.markdown("### 📋 GDPR Rights Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            **Implemented Rights:**
            - ✅ Right to Access (Role-based views)
            - ✅ Right to Rectification (Edit patient records)
            - ✅ Right to Erasure (Delete records)
            - ✅ Right to Data Portability (CSV export)
            - ✅ Right to be Informed (Consent banner)
        """)
    
    with col2:
        st.markdown("""
            **Security Measures:**
            - 🔒 Fernet Encryption (Reversible)
            - 🎭 Data Anonymization/Masking
            - 📋 Complete Audit Trail
            - 🔑 Role-Based Access Control
            - ⏰ Automated Data Retention
        """)

def show_footer():
    """Show system footer with uptime info"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
        <div class='footer'>
            🏥 Hospital Management System v1.0 | 
            GDPR Compliant | CIA Triad Implementation | 
            System Time: {current_time} | 
            ⚡ System Online
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Show consent banner if not shown
    if not st.session_state.consent_shown and not st.session_state.logged_in:
        show_consent_banner()
        return
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        login_page()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown(f"### 👤 Logged in as:")
            st.markdown(f"**{st.session_state.user['username']}**")
            st.markdown(f"Role: **{st.session_state.user['role'].upper()}**")
            st.markdown("---")
            
            # Navigation (informational)
            st.markdown("### 🧭 Navigation")
            if st.session_state.user['role'] == 'admin':
                st.info("Admin access: Full system control")
            elif st.session_state.user['role'] == 'doctor':
                st.info("Doctor access: View anonymized data")
            else:
                st.info("Receptionist: Add/Edit records")
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                db.log_action(st.session_state.user['user_id'], 
                            st.session_state.user['username'], 
                            st.session_state.user['role'], 
                            'logout', 
                            f"User {st.session_state.user['username']} logged out")
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.consent_shown = False
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 🛡️ CIA Triad")
            st.markdown("""
                - **🔒 Confidentiality**: Encryption & RBAC
                - **✅ Integrity**: Audit logs & validation
                - **🚀 Availability**: Stable access & backup
            """)
        
        # Route to appropriate dashboard
        if st.session_state.user['role'] == 'admin':
            admin_dashboard()
        elif st.session_state.user['role'] == 'doctor':
            doctor_dashboard()
        else:
            receptionist_dashboard()
        
        # Show footer
        show_footer()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"🚨 Application Error: {str(e)}")
        st.info("Please refresh the page or contact system administrator.")
