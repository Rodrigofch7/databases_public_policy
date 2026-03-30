# To edit: nano q1.sql
# To run: duckdb ev_data.db -> .read q1.sql

SELECT Model_Year, Model, Make
FROM VehicleModel
WHERE Model_ID = 510;

