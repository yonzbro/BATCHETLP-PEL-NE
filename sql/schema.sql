-- DDL Script for Batch ETL Pipeline (Star Schema Data Mart)

-- 1. Dimension Table: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY, -- Format: YYYYMMDD (e.g., 20260801)
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    day_of_week VARCHAR(15) NOT NULL
);

-- 2. Dimension Table: Currency
CREATE TABLE IF NOT EXISTS dim_currency (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR(3) UNIQUE NOT NULL,
    currency_name VARCHAR(50)
);

-- Initial seeding for dimension currencies
INSERT INTO dim_currency (currency_code, currency_name) VALUES
    ('TRY', 'Turkish Lira'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('JPY', 'Japanese Yen'),
    ('CAD', 'Canadian Dollar')
ON CONFLICT (currency_code) DO NOTHING;

-- 3. Fact Table: Daily Exchange Rates
CREATE TABLE IF NOT EXISTS fact_exchange_rates (
    fact_id SERIAL PRIMARY KEY,
    currency_id INT REFERENCES dim_currency(currency_id),
    date_id INT REFERENCES dim_date(date_id),
    rate_to_usd NUMERIC(18, 6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_currency_date UNIQUE (currency_id, date_id)
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_fact_date_id ON fact_exchange_rates(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_currency_id ON fact_exchange_rates(currency_id);
