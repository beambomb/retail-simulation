CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(16) NOT NULL,
    day_of_month INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(16) NOT NULL,
    quarter INT NOT NULL,
    year INT NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_payday BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    sku VARCHAR(32) NOT NULL,
    barcode VARCHAR(32) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    sell_price NUMERIC(12, 2) NOT NULL,
    margin_amount NUMERIC(12, 2) NOT NULL,
    margin_percentage NUMERIC(6, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_cashier (
    cashier_key SERIAL PRIMARY KEY,
    cashier_id VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    experience_level VARCHAR(16) NOT NULL,
    default_shift VARCHAR(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    persona VARCHAR(32) NOT NULL,
    has_loyalty BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key INT REFERENCES dim_product(product_key),
    cashier_key INT REFERENCES dim_cashier(cashier_key),
    customer_key INT REFERENCES dim_customer(customer_key),
    transaction_id VARCHAR(64) NOT NULL,
    item_id VARCHAR(64) NOT NULL,
    payment_method VARCHAR(32) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    gross_revenue NUMERIC(14, 2) NOT NULL,
    discount_amount NUMERIC(12, 2) NOT NULL,
    net_revenue NUMERIC(14, 2) NOT NULL,
    gross_profit NUMERIC(14, 2) NOT NULL,
    is_void BOOLEAN DEFAULT FALSE,
    error_flag VARCHAR(32) DEFAULT 'NONE'
);

CREATE TABLE IF NOT EXISTS fact_cashier_daily_performance (
    performance_key SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    cashier_key INT REFERENCES dim_cashier(cashier_key),
    counter_id INT NOT NULL,
    shift_type VARCHAR(16) NOT NULL,
    transactions_processed INT NOT NULL,
    errors_occurred INT NOT NULL,
    error_rate_pct NUMERIC(6, 2) NOT NULL,
    peak_fatigue NUMERIC(6, 4) NOT NULL
);
