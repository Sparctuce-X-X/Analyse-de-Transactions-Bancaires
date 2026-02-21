-- Table clients
CREATE TABLE IF NOT EXISTS clients (
client_id VARCHAR(50) PRIMARY KEY,
first_name VARCHAR(100),
last_name VARCHAR(100),
age INT,
gender VARCHAR(10),
city VARCHAR(100),
account_opening_date DATE
);
-- Table comptes
CREATE TABLE IF NOT EXISTS accounts (
account_id VARCHAR(50) PRIMARY KEY,
client_id VARCHAR(50) REFERENCES clients(client_id),
account_type VARCHAR(50),
branch_code VARCHAR(20),
account_balance DECIMAL(15,2),
opening_date DATE
);
-- Table transactions
CREATE TABLE IF NOT EXISTS transactions (
transaction_id SERIAL PRIMARY KEY,
account_id VARCHAR(50) REFERENCES accounts(account_id),
transaction_date TIMESTAMP,
transaction_type VARCHAR(50),
amount DECIMAL(15,2),
balance_after DECIMAL(15,2),
);


-- Index pour améliorer les performances
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);