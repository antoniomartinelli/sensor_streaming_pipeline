import requests
import pymongo
from time import sleep

drill_host = "drill"
mongo_host = "mongo"
batch_time = 5

url = "http://drill:8047/query.json"

payload="{\"queryType\":\"SQL\", \"query\": \"SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') AS `minute_timestamp`, AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value` FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro WHERE nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') >= DATE_SUB(CURRENT_TIMESTAMP, interval '5' minute) GROUP BY minute_timestamp\", \"autoLimit\":5}"

headers = {
  'Content-Type': 'application/json'
}

while (1):
    response = requests.request("POST", url, headers=headers, data=payload)

    myclient = pymongo.MongoClient("mongodb://admin1:admin1@mongo:27017/m_db")
    mydb = myclient["m_db"]
    mycol = mydb["batch_measure"]
    
    print("Query performed")
    print(response.json())
    #print(response.json()['rows'])

    for row in response.json()['rows']:
        mycol.insert_one(row)
    print("Stored in the database")
    sleep(60*batch_time)
