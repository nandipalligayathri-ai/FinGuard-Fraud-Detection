USE financial_risk_db;
INSERT IGNORE INTO customers (customer_code, full_name) VALUES
('CUST001', 'Demo Customer One'), ('CUST002', 'Demo Customer Two');
INSERT IGNORE INTO accounts (customer_id, account_number) VALUES
(1, 'DEMO-ACC-1001'), (2, 'DEMO-ACC-1002');
