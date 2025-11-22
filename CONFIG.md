# Hospital Management System Configuration

## System Information
- **Project Name**: GDPR-Compliant Hospital Management System
- **Version**: 1.0.0
- **Database**: SQLite (hospital_management.db)
- **Framework**: Streamlit
- **Encryption**: Fernet (symmetric)

## Default Settings

### Database Configuration
- Database file: `hospital_management.db`
- Auto-initialize: Yes
- Sample data: Included
- Backup: Manual (CSV export)

### Security Configuration
- Password hashing: SHA-256
- Encryption: Fernet
- Key file: `encryption.key`
- Session timeout: None (manual logout)

### GDPR Settings
- Data retention period: 30 days
- Auto-cleanup: Manual trigger
- Consent tracking: Enabled
- Audit logging: All actions

### Application Settings
- Port: 8501 (Streamlit default)
- Host: localhost
- Debug mode: False
- Auto-reload: True (development)

## User Roles and Permissions

### Admin
- Username: admin
- Password: admin123
- Permissions: Full system access

### Doctor
- Username: DrBob
- Password: doc123
- Permissions: View anonymized data only

### Receptionist
- Username: Alice_recep
- Password: rec123
- Permissions: Add/edit patient records

## File Structure

```
IS Assignment 4/
├── app.py                      # Main application
├── database.py                 # Database manager
├── run.py                      # Quick start script
├── requirements.txt            # Dependencies
├── Assignment4.ipynb           # Documentation
├── README.md                   # Full documentation
├── CONFIG.md                   # This file
├── hospital_management.db      # Database (auto-generated)
└── encryption.key              # Encryption key (auto-generated)
```

## Running the Application

### Method 1: Using run.py (Recommended)
```bash
python run.py
```

### Method 2: Direct Streamlit
```bash
streamlit run app.py
```

### Method 3: With specific port
```bash
streamlit run app.py --server.port 8502
```

## Environment Variables (Optional)

You can set these environment variables for custom configuration:

```bash
# Database name
export DB_NAME=hospital_management.db

# Encryption key file
export KEY_FILE=encryption.key

# Streamlit port
export STREAMLIT_SERVER_PORT=8501
```

## Troubleshooting

### Issue: Port already in use
**Solution**: Use a different port
```bash
streamlit run app.py --server.port 8502
```

### Issue: Dependencies not installed
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Database locked
**Solution**: Close any other connections to the database file

### Issue: Encryption key error
**Solution**: Delete `encryption.key` and restart (will generate new key)

## Security Notes

⚠️ **Important Security Considerations:**

1. **Change Default Passwords**: In production, change all default passwords
2. **Secure Key Storage**: Store `encryption.key` securely (not in version control)
3. **HTTPS**: Use HTTPS in production (Streamlit Cloud or reverse proxy)
4. **Database Security**: Use proper database security in production
5. **Regular Backups**: Schedule regular database backups
6. **Audit Review**: Regularly review audit logs

## Performance Optimization

### For Better Performance:
1. Enable caching for database connections
2. Index frequently queried columns
3. Limit log display to recent entries
4. Implement pagination for large datasets

### Database Indexes (if needed):
```sql
CREATE INDEX idx_patients_date ON patients(date_added);
CREATE INDEX idx_logs_timestamp ON logs(timestamp);
CREATE INDEX idx_logs_user ON logs(user_id);
```

## Backup Strategy

### Manual Backup
1. Export data using CSV export feature
2. Copy `hospital_management.db` file
3. Save `encryption.key` securely

### Automated Backup (Future)
- Schedule daily backups
- Cloud storage integration
- Versioned backups

## Monitoring

### Key Metrics to Monitor:
- Total patients
- Daily actions
- Anonymized records
- User activity
- System uptime

### Log Analysis:
- Check audit logs regularly
- Monitor for unauthorized access
- Review anonymization actions
- Track data retention cleanup

## Compliance

### GDPR Checklist:
- [x] Data minimization
- [x] Purpose limitation
- [x] Storage limitation (30 days)
- [x] Integrity and confidentiality
- [x] Accountability (audit logs)
- [x] User consent tracking
- [x] Right to access
- [x] Right to rectification
- [x] Right to erasure
- [x] Right to data portability

## Support

For technical issues:
1. Check README.md for detailed documentation
2. Review Assignment4.ipynb for code examples
3. Examine application logs
4. Check database integrity

## Updates and Maintenance

### Regular Maintenance Tasks:
- Run data retention cleanup
- Review and export audit logs
- Check system metrics
- Update dependencies
- Review user access

### Update Process:
1. Backup database
2. Update code files
3. Install new dependencies
4. Test functionality
5. Deploy changes

## Development Notes

### Adding New Features:
1. Update database schema if needed
2. Add new functions to database.py
3. Create UI components in app.py
4. Add logging for new actions
5. Update documentation

### Testing:
1. Test each user role
2. Verify all CRUD operations
3. Check audit logging
4. Test GDPR features
5. Verify error handling

## License and Credits

**Educational Project**
- Course: Information Security
- Institution: FAST University
- Semester: 7
- Date: November 2025

**Technologies Used:**
- Python 3.8+
- Streamlit
- SQLite
- Pandas
- Plotly
- Cryptography (Fernet)

---

*Configuration Guide v1.0.0*
*Last Updated: November 17, 2025*
