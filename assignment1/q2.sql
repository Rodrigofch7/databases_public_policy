# To edit: nano q2.sql
# To run: duckdb ev_data.db -> .read q2.sql

SELECT COUNT(DISTINCT Model) AS Num_Models
FROM VehicleModel
WHERE Base_MSRP = 0;
