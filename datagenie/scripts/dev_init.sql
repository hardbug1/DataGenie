-- DataGenie Development Database Setup
-- This script runs when the development PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set timezone
SET timezone = 'UTC';

-- Create development user with more permissions for testing
CREATE USER IF NOT EXISTS dev_user WITH PASSWORD 'dev_password';
GRANT ALL PRIVILEGES ON DATABASE datagenie_dev TO dev_user;

-- Development-specific settings
ALTER DATABASE datagenie_dev SET log_statement = 'all';
ALTER DATABASE datagenie_dev SET log_duration = on;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'DataGenie DEVELOPMENT database initialization completed at %', now();
    RAISE NOTICE 'Development mode: Enhanced logging enabled';
END $$;
