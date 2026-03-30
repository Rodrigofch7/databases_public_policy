# To edit: nano q3.sql
# To run: duckdb ev_data.db -> .read q3.sql

SELECT DOL_Vehicle_ID
FROM Registration
ORDER BY Model_ID DESC
LIMIT 1;
