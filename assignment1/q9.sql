SELECT
    l.County,
    COUNT(r.DOL_Vehicle_ID) AS Total_Registered,
    (SUM(CASE WHEN vm.Vehicle_Type = 'Battery Electric Vehicle (BEV)' 
              THEN 1.0 ELSE 0 END) 
     / COUNT(r.DOL_Vehicle_ID) * 100) AS BEV_Percentage
FROM Registration r
JOIN Location l ON r.City = l.City AND r.County = l.County
JOIN VehicleModel vm ON r.Model_ID = vm.Model_ID
GROUP BY l.County
HAVING (SUM(CASE WHEN vm.Vehicle_Type = 'Battery Electric Vehicle (BEV)' 
                 THEN 1.0 ELSE 0 END) 
        / COUNT(r.DOL_Vehicle_ID) * 100) > 50
ORDER BY BEV_Percentage DESC, Total_Registered DESC, l.County ASC;
