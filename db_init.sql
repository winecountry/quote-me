DROP ROLE IF EXISTS quote_admin;
CREATE ROLE quote_admin LOGIN PASSWORD 'password';

ALTER ROLE quote_admin SET client_encoding TO 'utf8';
ALTER ROLE quote_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE quote_admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE quote_db TO quote_admin;
