-- RFP Automation System Database Schema

-- RFPs table
CREATE TABLE IF NOT EXISTS rfps (
    rfp_id VARCHAR(50) PRIMARY KEY,
    title TEXT NOT NULL,
    source TEXT,
    deadline TIMESTAMP,
    scope TEXT,
    testing_requirements JSONB,
    specifications JSONB,
    status VARCHAR(20) DEFAULT 'new',
    match_score FLOAT,
    total_estimate DECIMAL(12,2),
    recommended_sku VARCHAR(50),
    discovered_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rfps_status ON rfps(status);
CREATE INDEX idx_rfps_deadline ON rfps(deadline);
CREATE INDEX idx_rfps_discovered_at ON rfps(discovered_at);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    sku VARCHAR(50) PRIMARY KEY,
    product_name TEXT NOT NULL,
    category VARCHAR(100),
    manufacturer VARCHAR(100),
    specifications JSONB NOT NULL,
    unit_price DECIMAL(10,2),
    stock_status VARCHAR(50),
    datasheet_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_manufacturer ON products(manufacturer);
CREATE INDEX idx_products_name ON products(product_name);

-- Product matches table
CREATE TABLE IF NOT EXISTS product_matches (
    match_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE CASCADE,
    sku VARCHAR(50) REFERENCES products(sku),
    product_name TEXT,
    match_score FLOAT NOT NULL,
    specification_alignment JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_matches_rfp_id ON product_matches(rfp_id);
CREATE INDEX idx_product_matches_sku ON product_matches(sku);
CREATE INDEX idx_product_matches_score ON product_matches(match_score DESC);

-- Pricing breakdown table
CREATE TABLE IF NOT EXISTS pricing_breakdown (
    pricing_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE CASCADE,
    sku VARCHAR(50) REFERENCES products(sku),
    unit_price DECIMAL(12,2) NOT NULL,
    quantity INTEGER NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    testing_cost DECIMAL(12,2),
    delivery_cost DECIMAL(12,2),
    urgency_adjustment DECIMAL(12,2),
    total DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pricing_breakdown_rfp_id ON pricing_breakdown(rfp_id);
CREATE INDEX idx_pricing_breakdown_sku ON pricing_breakdown(sku);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id SERIAL PRIMARY KEY,
    rfp_id VARCHAR(50) REFERENCES rfps(rfp_id) ON DELETE CASCADE,
    outcome VARCHAR(20) NOT NULL,
    actual_price DECIMAL(12,2),
    predicted_price DECIMAL(12,2),
    match_accuracy FLOAT,
    notes TEXT,
    submitted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feedback_rfp_id ON feedback(rfp_id);
CREATE INDEX idx_feedback_outcome ON feedback(outcome);
CREATE INDEX idx_feedback_submitted_at ON feedback(submitted_at);

-- Performance metrics table
CREATE TABLE IF NOT EXISTS performance_metrics (
    metric_id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_metrics_name ON performance_metrics(metric_name);
CREATE INDEX idx_metrics_period ON performance_metrics(period_start, period_end);

-- Model versions table
CREATE TABLE IF NOT EXISTS model_versions (
    version_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    model_path TEXT,
    performance_metrics JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_model_versions_name ON model_versions(model_name);
CREATE INDEX idx_model_versions_active ON model_versions(is_active);

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

CREATE INDEX idx_emails_status ON emails(status);
CREATE INDEX idx_emails_rfp_id ON emails(rfp_id);
CREATE INDEX idx_emails_received_at ON emails(received_at);

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

CREATE INDEX idx_audit_rfp_id ON audit_reports(rfp_id);
CREATE INDEX idx_audit_timestamp ON audit_reports(audit_timestamp);
CREATE INDEX idx_audit_recommendation ON audit_reports(overall_recommendation);
