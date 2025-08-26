-- DataGenie Initial Database Setup
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create initial database if it doesn't exist
-- (This is handled by POSTGRES_DB environment variable)

-- Set timezone
SET timezone = 'UTC';

-- Create basic database structure will be handled by Alembic migrations
-- This file is mainly for extensions and initial setup

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE 'DataGenie database initialization completed at %', now();
END $$;
