# Sensor Streaming Lakehouse

## Instruction
The entire stack runs on containerized Docker services.
1. Run *start.sh*

## Pipeline

* Data Generator (generator)
  - Generate fake data for a sensor and publish them on a Kafka topic

* Kafka Broker (broker)
  - Listen to specific Kafka topic and forward the messages to other services

* MongoDB-Sink (connect)
  - Listen to specific Kafka topic and store the messages in MongoDB

* MongoDB (mongo)
  - Store the messages received

* Apache Drill (drill)
  - Query the database via SQL queries
  - Expose REST APIs to execute queries

* Scheduled Aggregator (sched_aggregator)
  - Runs scheduled aggregation tasks through Drill, store the output in MongoDB

# Snippets

```bash
mongosh "mongodb://localhost:27017/m_db" --username admin1 --password admin1
```

```sql
SELECT * FROM mongo.m_db.measure;
```

```sql
SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') AS `minute_timestamp`, 
       AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value`
    FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro
    GROUP BY minute_timestamp;
```

# References
* https://florimond.dev/en/posts/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/
* https://github.com/florimondmanca/kafka-fraud-detector
* https://github.com/RWaltersMA/mongo-source-sink
* https://github.com/mongodb/mongo-kafka
