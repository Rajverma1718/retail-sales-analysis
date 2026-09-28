-- Retail Sales Analysis SQL practice queries

-- 1. Revenue and profit by category
SELECT category,
       SUM(quantity * unit_price) AS revenue,
       SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 2. Monthly performance
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(quantity * unit_price) AS revenue,
       SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales
GROUP BY month
ORDER BY month;

-- 3. Regional ranking using a window function
WITH regional_sales AS (
    SELECT region, SUM(quantity * unit_price) AS revenue
    FROM sales
    GROUP BY region
)
SELECT region, revenue,
       RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM regional_sales;

-- 4. Customer segment contribution
SELECT customer_segment,
       COUNT(DISTINCT order_id) AS orders,
       SUM(quantity * unit_price) AS revenue,
       AVG(quantity * unit_price) AS average_order_value
FROM sales
GROUP BY customer_segment
ORDER BY revenue DESC;
