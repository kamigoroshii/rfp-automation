-- Quick Migration: Add emails and audit_reports tables
-- Run this with: psql -U postgres -d rfp_automation -f quick_migration.sql

-- Emails table (for email monitoring)
CREATE TABLE IF NOT EXISTS emails (
    email_id VARCHAR(50) PRIMARY KEY,
    subject TEXT NOT NULL,
    sender VARCHAR(255),
    received_at TIMESTAMP,
    body TEXT,
    attachments JSONB,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE SET NULL,
    status VARCHAR(20) DEFAULT 'pending',
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_emails_status ON emails(status);
CREATE INDEX IF NOT EXISTS idx_emails_rfp_id ON emails(rfp_id);
CREATE INDEX IF NOT EXISTS idx_emails_received_at ON emails(received_at);

-- Audit reports table (for auditor agent)
CREATE TABLE IF NOT EXISTS audit_reports (
    audit_id VARCHAR(50) PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE CASCADE,
    audit_timestamp TIMESTAMP DEFAULT NOW(),
    overall_recommendation VARCHAR(20) NOT NULL,
    compliance_score FLOAT,
    critical_issues_count INTEGER DEFAULT 0,
    summary TEXT,
    rfp_validation JSONB,
    match_validation JSONB,
    pricing_validation JSONB,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_rfp_id ON audit_reports(rfp_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_reports(audit_timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_recommendation ON audit_reports(overall_recommendation);

-- Verify tables created
SELECT 'emails' as table_name, COUNT(*) as row_count FROM emails
UNION ALL
SELECT 'audit_reports' as table_name, COUNT(*) as row_count FROM audit_reports;

\echo '✅ Migration complete! Tables created successfully.'
