-- Create database if not exists
CREATE DATABASE my_database;

-- Connect to the database
\c my_database;

-- Create extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create function for updating timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
