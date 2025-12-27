-- Rush hours and days
SELECT 
    order_dow AS day_of_week,
    order_hour_of_day AS hour_of_day,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY order_dow, order_hour_of_day
ORDER BY total_orders DESC
LIMIT 10;
-- Mostly the most rush are in Mondays and Sundays during day (10-> 15)
------------------------------------------------------------------------
--What are the top selling products?
SELECT 
    p.product_name,
    COUNT(op.product_id) AS times_ordered
FROM order_products op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_name
ORDER BY times_ordered DESC
LIMIT 10;

-----------------------------------------------------
--Which products drive customer loyalty? "Products that have high re-order Rate"
SELECT 
    p.product_name,
    COUNT(op.product_id) AS total_sales,
    round(AVG(op.reordered),3) AS reorder_rate
FROM order_products op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_name
HAVING COUNT(op.product_id) > 1000 -- Filter out noise (items sold rarely)
ORDER BY reorder_rate DESC
LIMIT 10;

-----------------------------------------------------
-- Pareto Analysis
WITH ProductSales AS (
    -- 1. Get raw volume per product
    SELECT 
        p.product_name,
        COUNT(*) as total_sales
    FROM order_products op
    JOIN products p ON op.product_id = p.product_id
    GROUP BY p.product_name
),
RunningTotal AS (
    -- 2. Calculate Cumulative Sum and Total Market Volume
    SELECT 
        product_name,
        total_sales,
        SUM(total_sales) OVER (ORDER BY total_sales DESC) as running_sum,
        SUM(total_sales) OVER () as total_market_volume
    FROM ProductSales
)
-- 3. Calculate Cumulative %
SELECT 
    product_name,
    total_sales,
    ROUND((running_sum::numeric / total_market_volume) * 100, 2) as cumulative_percent
FROM RunningTotal
WHERE (running_sum::numeric / total_market_volume) <= 0.80 
ORDER BY total_sales DESC;



-- Basket Size Central Tendency
WITH BasketSizes AS (
-- Number of Products in each order
    SELECT 
        order_id, 
        COUNT(product_id) as items_in_cart
    FROM order_products
    GROUP BY order_id
)
SELECT 
    AVG(items_in_cart) as mean_basket_size,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY items_in_cart) as median_basket_size,
    MIN(items_in_cart) as smallest_order,
    MAX(items_in_cart) as largest_order
FROM BasketSizes;

-- Mean > Median --> Right skewed data

------------------------------------------------------------
-- Customer Segmentation
SELECT 
    days_since_prior_order,
    COUNT(*) as frequency,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders)), 2) as percentage_of_total_orders
FROM orders
WHERE days_since_prior_order IS NOT NULL
GROUP BY days_since_prior_order
ORDER BY percentage_of_total_orders Desc;

------------------------------------------------------------
--Cross-selling Analysis
-- Which departments are more trustworthy for customers? and Which are interchangeable?
SELECT 
    d.department,
    COUNT(op.order_id) as total_items_sold,
    ROUND(AVG(op.reordered), 2) as retention_rate -- 
FROM order_products op
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY retention_rate DESC;

-------------------------------------------------------------

-- Order Sequence Analysis (Cohort Behavior)
SELECT 
    order_number, 
    ROUND(AVG(days_since_prior_order)::numeric, 1) as avg_days_between_orders,
    COUNT(order_id) as total_orders_at_this_stage
FROM orders
WHERE order_number <= 20 
GROUP BY order_number
ORDER BY order_number;
-- Customers are developing a habit of buying




