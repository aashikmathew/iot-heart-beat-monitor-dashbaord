-- Initialize IoT Heartbeat Monitor Database
-- This script runs when the PostgreSQL container starts for the first time

-- Create the database (if not exists)
-- Note: The database is already created by POSTGRES_DB environment variable

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The actual tables will be created by SQLAlchemy when the app starts
-- This file can be used for any additional database setup if needed

-- Create some indexes for better performance
-- (These will be created by SQLAlchemy, but we can add custom ones here if needed)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE iot_heartbeat TO iot_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO iot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO iot_user; 