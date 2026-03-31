SELECT 
    l.County,
    COUNT(r.DOL_Vehicle_ID) AS Num_Registered,
    AVG(vm.Base_MSRP) AS Avg_Base_MSRP
FROM Location l
JOIN Registration r ON l.City = r.City AND l.County = r.County
JOIN VehicleModel vm ON r.Model_ID = vm.Model_ID
WHERE l.State = 'WA'
GROUP BY l.County
ORDER BY Avg_Base_MSRP DESC, l.County ASC;
