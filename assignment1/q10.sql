# To edit: nano q10.sql
# To run: duckdb ev_data.db -> .read q10.sql

WITH CountyRegistrations AS (
    SELECT l.County
    FROM Registration r
    JOIN Location l ON r.City = l.City AND r.County = l.County
    GROUP BY l.County
    HAVING COUNT(r.DOL_Vehicle_ID) > 100
),
EligibleModels AS (
    SELECT DISTINCT vm.Make, vm.Model, vm.Base_MSRP
    FROM VehicleModel vm
    JOIN Registration r ON vm.Model_ID = r.Model_ID
    JOIN Location l ON r.City = l.City AND r.County = l.County
    WHERE l.County IN (SELECT County FROM CountyRegistrations)
)
SELECT DISTINCT e1.Make, e1.Model
FROM EligibleModels e1
JOIN EligibleModels e2 ON e1.Make = e2.Make
    AND e1.Model != e2.Model
    AND e1.Base_MSRP <= e2.Base_MSRP - 5000
ORDER BY e1.Model ASC;
