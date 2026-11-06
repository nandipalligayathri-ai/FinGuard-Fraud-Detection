CREATE DATABASE IF NOT EXISTS financial_risk_db;
USE financial_risk_db;

CREATE TABLE IF NOT EXISTS customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_code VARCHAR(30) NOT NULL UNIQUE,
  full_name VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS accounts (
  account_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  account_number VARCHAR(30) NOT NULL UNIQUE,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE IF NOT EXISTS transactions (
  transaction_id INT AUTO_INCREMENT PRIMARY KEY,
  account_id INT NOT NULL,
  transaction_datetime DATETIME NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  transaction_type VARCHAR(30) NOT NULL,
  channel VARCHAR(30) NOT NULL,
  region VARCHAR(80),
  INDEX idx_transaction_time (transaction_datetime),
  FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
CREATE TABLE IF NOT EXISTS alerts (
  alert_id INT AUTO_INCREMENT PRIMARY KEY,
  transaction_id INT NOT NULL,
  rule_name VARCHAR(100) NOT NULL,
  risk_score INT NOT NULL,
  review_status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
  reason TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  reviewed_at DATETIME,
  FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);
CREATE TABLE IF NOT EXISTS users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  is_active BOOLEAN DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS audit_logs (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL,
  action VARCHAR(100) NOT NULL,
  details TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
