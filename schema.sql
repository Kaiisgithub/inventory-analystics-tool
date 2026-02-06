-- Create the Transaction Table
CREATE TABLE daily_inventory (
    date DATE,
    product_id INT,
    qty INT,
    type VARCHAR(20) -- 'SALE' or 'RESTOCK'
);

-- Become a 'DASHBOARD' and udpate depend on the CASE
CREATE VIEW stock_dashboard AS
SELECT 
    product_id,
    SUM(qty) as total_stock,
    CASE 
        WHEN SUM(qty) < 5 THEN 'CRITICAL LOW'
        WHEN SUM(qty) >= 5 AND SUM(qty) < 15 THEN 'Running Low'
        ELSE 'OK'
    END as status
FROM daily_inventory
GROUP BY product_id;
