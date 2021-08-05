"""Produce fake transactions into a Kafka topic via Avro."""

import os
from time import sleep
import json

from kafka import KafkaProducer
from transactions import create_random_transaction


from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer


value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "timestamp",
       "type" : "int"
     },
     {
       "name" : "value",
       "type" : "float"
     }
   ]
}
"""

key_schema_str = """
{
   "namespace": "my.test",
   "name": "key",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)
value = {"name": "Value"}
key = {"name": "ThisisaKey"}


TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

if __name__ == '__main__':
    sleep(50)
    #producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
    #    value_serializer=lambda value: json.dumps(value).encode(),
    #)
    avroProducer = AvroProducer({
    'bootstrap.servers': KAFKA_BROKER_URL,
    'on_delivery': delivery_report,
    'schema.registry.url': 'http://schema-registry:8081'
    }, default_key_schema=key_schema, default_value_schema=value_schema)

    print("Starting measurements #####################")
    while True:
        transaction: dict = create_random_transaction()
        value = {"timestamp": transaction['timestamp'], "value": transaction['value'] }
        key = {"name": str(transaction['timestamp'])}
        avroProducer.produce(topic=TRANSACTIONS_TOPIC, value=value, key=key)
        print(transaction)  # DEBUG
        sleep(SLEEP_TIME)

#avroProducer.flush()
