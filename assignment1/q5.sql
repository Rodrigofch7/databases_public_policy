# To edit: nano q5.sql
# To run: duckdb ev_data.db -> .read q5.sql

SELECT 
    Model,
    Make,
    Model_Year
FROM VehicleModel
WHERE CAFV_Eligibility != 'Clean Alternative Fuel Vehicle Eligible'
  AND Electric_Range = (
      SELECT MAX(Electric_Range)
      FROM VehicleModel
      WHERE CAFV_Eligibility != 'Clean Alternative Fuel Vehicle Eligible'
  )
ORDER BY Model ASC, Make ASC, Model_Year ASC;
