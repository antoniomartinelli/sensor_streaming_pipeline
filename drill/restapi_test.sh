#!/bin/bash
curl -X POST -H "Content-Type: application/json" \
-d '{"queryType":"SQL", "query": "SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), '\''MINUTE'\'') AS `minute_timestamp`, AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value` FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro GROUP BY minute_timestamp", "autoLimit":10}' http://localhost:8047/query.json

curl -X POST -H "Content-Type: application/json" \ 
-d '{"queryType":"SQL", "query": "SELECT * FROM mongo.m_db.measure", "autoLimit":10}' http://localhost:8047/query.json
