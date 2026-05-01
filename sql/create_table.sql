-- ============================================
-- create_tables.sql
-- Schéma BigQuery pour héberger les ventes de chaussures.
-- ============================================

CREATE SCHEMA IF NOT EXISTS `shoes_sales`;

-- ============================================
-- Table principale : 1 ligne par transaction
-- ============================================
CREATE OR REPLACE TABLE `shoes_sales.transactions` (
    Sale_ID         STRING    NOT NULL,
    Date            DATE      NOT NULL,
    Brand           STRING    NOT NULL,
    Shoe_Type       STRING    NOT NULL,
    Color           STRING    NOT NULL,
    Country         STRING    NOT NULL,
    Sales_Channel   STRING    NOT NULL,
    Price_USD       FLOAT64   NOT NULL,
    Units_Sold      INT64     NOT NULL,
    Revenue_USD     FLOAT64   NOT NULL,

    -- Features dérivées
    Year            INT64,
    Month           INT64,
    YearMonth       STRING,
    Quarter         STRING,
    Season          STRING,
    DayOfWeek       STRING,
    WeekOfYear      INT64,
    Price_Bucket    STRING,
    Revenue_Bucket  STRING
)
PARTITION BY Date
CLUSTER BY Brand, Country, Sales_Channel;


-- ============================================
-- Datamarts
-- ============================================

CREATE OR REPLACE TABLE `shoes_sales.dm_brand_performance` (
    Brand              STRING,
    sales              INT64,
    total_revenue      FLOAT64,
    total_units        INT64,
    avg_price          FLOAT64,
    avg_order_value    FLOAT64,
    market_share_pct   FLOAT64
);

CREATE OR REPLACE TABLE `shoes_sales.dm_country_performance` (
    Country            STRING,
    sales              INT64,
    total_revenue      FLOAT64,
    total_units        INT64,
    avg_price          FLOAT64,
    avg_order_value    FLOAT64,
    market_share_pct   FLOAT64
);

CREATE OR REPLACE TABLE `shoes_sales.dm_channel_performance` (
    Sales_Channel      STRING,
    sales              INT64,
    total_revenue      FLOAT64,
    total_units        INT64,
    avg_order_value    FLOAT64,
    avg_price          FLOAT64,
    market_share_pct   FLOAT64
);

CREATE OR REPLACE TABLE `shoes_sales.dm_monthly_trend` (
    YearMonth          STRING,
    sales              INT64,
    total_revenue      FLOAT64,
    total_units        INT64,
    avg_order_value    FLOAT64
);