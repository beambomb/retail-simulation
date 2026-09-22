CREATE TABLE IF NOT EXISTS stores (
    store_id VARCHAR(32) PRIMARY KEY,
    store_name VARCHAR(128) NOT NULL,
    address TEXT,
    city VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cashiers (
    cashier_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    experience_level VARCHAR(16) NOT NULL,
    default_shift VARCHAR(16) NOT NULL,
    assigned_counter INT NOT NULL,
    base_error_rate NUMERIC(5, 4) DEFAULT 0.02
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    persona VARCHAR(32) NOT NULL,
    has_loyalty BOOLEAN DEFAULT FALSE,
    phone_number VARCHAR(32),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    sku VARCHAR(32) PRIMARY KEY,
    barcode VARCHAR(32) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    cost_price NUMERIC(12, 2) NOT NULL,
    sell_price NUMERIC(12, 2) NOT NULL,
    stock_on_hand INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    transaction_id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(32) REFERENCES stores(store_id),
    cashier_id VARCHAR(32) REFERENCES cashiers(cashier_id),
    customer_id VARCHAR(32),
    timestamp TIMESTAMP NOT NULL,
    payment_method VARCHAR(32) NOT NULL,
    total_amount NUMERIC(14, 2) NOT NULL,
    item_count INT NOT NULL,
    has_error BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id VARCHAR(64) PRIMARY KEY,
    transaction_id VARCHAR(64) REFERENCES orders(transaction_id) ON DELETE CASCADE,
    sequence INT NOT NULL,
    sku VARCHAR(32) REFERENCES products(sku),
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    subtotal NUMERIC(14, 2) NOT NULL,
    discount_applied NUMERIC(12, 2) DEFAULT 0.0,
    is_void BOOLEAN DEFAULT FALSE,
    error_type VARCHAR(32) DEFAULT 'NONE'
);

CREATE TABLE IF NOT EXISTS cashier_shifts (
    shift_id VARCHAR(64) PRIMARY KEY,
    cashier_id VARCHAR(32) REFERENCES cashiers(cashier_id),
    counter_id INT NOT NULL,
    shift_date DATE NOT NULL,
    shift_type VARCHAR(16) NOT NULL,
    transactions_processed INT DEFAULT 0,
    errors_occurred INT DEFAULT 0,
    peak_fatigue NUMERIC(6, 4) DEFAULT 0.0
);
