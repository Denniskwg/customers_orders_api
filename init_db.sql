-- Create a new database
CREATE DATABASE customers_orders_db;

-- Create a new user
CREATE USER dennis WITH ENCRYPTED PASSWORD 'dkamau476';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE customers_orders_db TO dennis;
-- Grant USAGE on public schema to the user
GRANT ALL PRIVILEGES ON SCHEMA public TO dennis;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dennis;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dennis;
