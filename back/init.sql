-- Create the database
CREATE DATABASE flask_db;

-- Connect to the new database
\c flask_db

-- Create a new role named 'root'
CREATE ROLE root WITH LOGIN PASSWORD '123';

-- Grant all privileges on the database to the role 'root'
GRANT ALL PRIVILEGES ON DATABASE flask_db TO root;

-- Optionally, create a schema if needed
CREATE SCHEMA my_schema AUTHORIZATION root;

-- Grant all privileges on the schema to the role 'root'
GRANT ALL PRIVILEGES ON SCHEMA my_schema TO root;

-- Create the table with the role 'root' as the owner
CREATE TABLE my_schema."user" (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant all privileges on the table to the role 'root'
GRANT ALL PRIVILEGES ON TABLE my_schema."user" TO root;
