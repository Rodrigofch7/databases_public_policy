# To edit: nano q6.sql
# To run: duckdb ev_data.db -> .read q6.sql

SELECT 
    l.County,
    AVG(vm.Model_Year) AS Avg_Model_Year
FROM Registration r
JOIN Location l ON r.City = l.City AND r.County = l.County
JOIN VehicleModel vm ON r.Model_ID = vm.Model_ID
WHERE vm.Electric_Range > 100
GROUP BY l.County
ORDER BY Avg_Model_Year DESC, l.County ASC
LIMIT 1;
