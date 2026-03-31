SELECT
    vm.Make,
    AVG(vm.Base_MSRP) AS Avg_Base_MSRP
FROM VehicleModel vm
JOIN Registration r ON vm.Model_ID = r.Model_ID
JOIN Location l ON r.City = l.City AND r.County = l.County
GROUP BY vm.Make
HAVING COUNT(DISTINCT l.City) > 1
ORDER BY Avg_Base_MSRP DESC, vm.Make ASC;
