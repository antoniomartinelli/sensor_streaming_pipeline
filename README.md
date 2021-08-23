# Sensor Streaming Lakehouse

## Instruction
The entire stack runs on containerized Docker services.
1. Run *start.sh*
2. (Optional) Use *ngrok tcp 27017* to expose mongoDB to external dashboards

## Pipeline

* Data Generator (generator)
  - Generate fake data for a sensor and publish them on a Kafka topic

* Kafka Broker (broker)
  - Listen to specific Kafka topic and forward the messages to other services

* MongoDB-Sink (connect)
  - Listen to specific Kafka topic and store the messages in MongoDB

* MongoDB (mongo)
  - Store the messages received and the aggregated values from the scheduled task

* Apache Drill (drill)
  - Query the database via SQL queries
  - Expose REST APIs to execute queries

* Scheduled Aggregator (sched_aggregator)
  - Runs scheduled aggregation tasks through Drill, store the output in MongoDB
  - Evaluate temporal mean on each minute
  - The task is scheduled to run every  5 minutes
  - Only the last 5 minutes are evaluated

# Snippets
* Access to MongoDB via MongoShell
```bash
mongosh "mongodb://localhost:27017/m_db" --username admin1 --password admin1
```

* Select all measurements stored in the db 
```sql
SELECT * FROM mongo.m_db.measure;
```

* Evaluate 1-minute mean for the measurement 
```sql
SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') AS `minute_timestamp`, 
       AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value`
    FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro
    GROUP BY minute_timestamp;
```

* Evaluate 1-minute mean for the measurement for the last 5 minutes
```sql
SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') AS `minute_timestamp`, 
        AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value` 
        FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro 
        WHERE nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') >= DATE_SUB(CURRENT_TIMESTAMP, interval '"+str(batch_time)+"' minute) 
        GROUP BY minute_timestamp
```

# References
* https://florimond.dev/en/posts/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/
* https://github.com/florimondmanca/kafka-fraud-detector
* https://github.com/RWaltersMA/mongo-source-sink
* https://github.com/mongodb/mongo-kafka
