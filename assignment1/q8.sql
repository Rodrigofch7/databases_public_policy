# To edit: nano q8.sql
# To run: duckdb ev_data.db -> .read q8.sql

SELECT
    vm.Make,
    vm.Model
FROM VehicleModel vm
JOIN Registration r ON vm.Model_ID = r.Model_ID
JOIN Location l ON r.City = l.City AND r.County = l.County
WHERE l.City = (
    SELECT l2.City
    FROM Registration r2
    JOIN Location l2 ON r2.City = l2.City AND r2.County = l2.County
    GROUP BY l2.City
    ORDER BY COUNT(*) DESC
    LIMIT 1
)
AND vm.Base_MSRP = (
    SELECT MAX(vm2.Base_MSRP)
    FROM VehicleModel vm2
    JOIN Registration r2 ON vm2.Model_ID = r2.Model_ID
    JOIN Location l2 ON r2.City = l2.City AND r2.County = l2.County
    WHERE l2.City = (
        SELECT l3.City
        FROM Registration r3
        JOIN Location l3 ON r3.City = l3.City AND r3.County = l3.County
        GROUP BY l3.City
        ORDER BY COUNT(*) DESC
        LIMIT 1
    )
)
GROUP BY vm.Make, vm.Model
ORDER BY vm.Make ASC, vm.Model ASC;
