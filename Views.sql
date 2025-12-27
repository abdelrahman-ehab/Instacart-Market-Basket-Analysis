-- Creating Views for Power BI 
CREATE OR REPLACE VIEW v_executive_summary AS
SELECT 
    order_dow,
    order_hour_of_day,
    COUNT(order_id) AS total_orders,
    AVG(days_since_prior_order) AS avg_days_since_order
FROM orders
GROUP BY order_dow, order_hour_of_day;

----------------------------------------
CREATE OR REPLACE VIEW v_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    d.department,
    COUNT(op.order_id) AS total_sales,
    AVG(op.reordered) AS reorder_rate
FROM order_products op
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY p.product_id, p.product_name, d.department;


-------------------------------------------
CREATE OR REPLACE VIEW v_cohort_analysis AS
SELECT 
    order_number,
    COUNT(order_id) AS total_orders,
    AVG(days_since_prior_order) AS avg_days_gap
FROM orders
WHERE order_number <= 50 
GROUP BY order_number;