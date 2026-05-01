-- ============================================
-- queries.sql
-- Requêtes analytiques pour Looker Studio
-- ============================================

-- 1. KPIs globaux
SELECT
    COUNT(*)                              AS total_sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    SUM(Units_Sold)                       AS total_units,
    ROUND(AVG(Revenue_USD), 2)            AS avg_order_value,
    ROUND(AVG(Price_USD), 2)              AS avg_price,
    COUNT(DISTINCT Brand)                 AS unique_brands,
    COUNT(DISTINCT Country)               AS unique_countries
FROM `shoes_sales.transactions`;


-- 2. Performance par marque + market share
SELECT
    Brand,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    SUM(Units_Sold)                       AS total_units,
    ROUND(AVG(Price_USD), 2)              AS avg_price,
    ROUND(100 * SUM(Revenue_USD) / SUM(SUM(Revenue_USD)) OVER (), 2) AS market_share_pct
FROM `shoes_sales.transactions`
GROUP BY Brand
ORDER BY total_revenue DESC;


-- 3. Top pays par revenus
SELECT
    Country,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    ROUND(AVG(Revenue_USD), 2)            AS avg_order_value
FROM `shoes_sales.transactions`
GROUP BY Country
ORDER BY total_revenue DESC;


-- 4. Évolution mensuelle (saisonnalité)
SELECT
    YearMonth,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    SUM(Units_Sold)                       AS units_sold
FROM `shoes_sales.transactions`
GROUP BY YearMonth
ORDER BY YearMonth;


-- 5. Performance par canal
SELECT
    Sales_Channel,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    ROUND(AVG(Revenue_USD), 2)            AS avg_order_value,
    ROUND(100 * SUM(Revenue_USD) / SUM(SUM(Revenue_USD)) OVER (), 2) AS share_pct
FROM `shoes_sales.transactions`
GROUP BY Sales_Channel
ORDER BY total_revenue DESC;


-- 6. Matrice marque × pays
SELECT
    Brand, Country,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS revenue
FROM `shoes_sales.transactions`
GROUP BY Brand, Country
ORDER BY Brand, revenue DESC;


-- 7. Top 10 transactions
SELECT
    Sale_ID, Date, Brand, Shoe_Type, Country,
    Price_USD, Units_Sold, Revenue_USD
FROM `shoes_sales.transactions`
ORDER BY Revenue_USD DESC
LIMIT 10;


-- 8. Performance par tranche de prix
SELECT
    Price_Bucket,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    ROUND(AVG(Units_Sold), 2)             AS avg_units_per_sale
FROM `shoes_sales.transactions`
GROUP BY Price_Bucket
ORDER BY total_revenue DESC;


-- 9. Saisonnalité
SELECT
    Season,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS total_revenue,
    ROUND(100 * SUM(Revenue_USD) / SUM(SUM(Revenue_USD)) OVER (), 2) AS pct_of_year
FROM `shoes_sales.transactions`
GROUP BY Season
ORDER BY total_revenue DESC;


-- 10. Top combinaisons couleur × type
SELECT
    Color, Shoe_Type,
    COUNT(*)                              AS sales,
    ROUND(SUM(Revenue_USD), 2)            AS revenue
FROM `shoes_sales.transactions`
GROUP BY Color, Shoe_Type
ORDER BY revenue DESC
LIMIT 10;