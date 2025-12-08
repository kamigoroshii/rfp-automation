-- Create PostgreSQL user for RFP Automation System
-- Run this as the postgres superuser

-- Create user if it doesn't exist
DO
$$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'rfp_user') THEN
    CREATE USER rfp_user WITH PASSWORD 'your_secure_password_here';
  END IF;
END
$$;

-- Grant necessary privileges
ALTER USER rfp_user CREATEDB;

-- Grant connection privileges
GRANT CONNECT ON DATABASE postgres TO rfp_user;

-- Success message
\echo 'User rfp_user created successfully!'
\echo 'Now you can run: python shared/database/init_db.py'
