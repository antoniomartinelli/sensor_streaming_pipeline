import requests
import pymongo
from time import sleep

drill_host = "drill"
mongo_host = "mongo"
batch_time = 5 # minutes

url = "http://"+drill_host+":8047/query.json"

#SQL query: evaluate temporal mean aggregation on minute basis every (batch_time) minutes
payload="{\"queryType\":\"SQL\", \"query\": \"SELECT nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') AS `minute_timestamp`, AVG(CAST(`right`(macro.macro_val.`value`,6) AS float) ) AS `measure_value` FROM (SELECT value as macro_val FROM mongo.m_db.measure) macro WHERE nearestDate(TO_TIMESTAMP(CAST(macro.macro_val.`timestamp` AS int)), 'MINUTE') >= DATE_SUB(CURRENT_TIMESTAMP, interval '"+str(batch_time)+"' minute) GROUP BY minute_timestamp\", \"autoLimit\":5}"

headers = {
  'Content-Type': 'application/json'
}

# Pymongo init
myclient = pymongo.MongoClient("mongodb://admin1:admin1@mongo:27017/m_db")
mydb = myclient["m_db"]
mycol = mydb["batch_measure"]

while (1):
    # Make REST-API request with the aggregation query
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print("Aggregation query performed succesfully")
        print(response.json())
    else:
        print("Aggregation query error")
        print(response.json())
        exit()
        
    # Insert in the DB for the aggregated values
    for row in response.json()['rows']:
        mycol.insert_one(row)
    print("Stored in the database")
    sleep(60*batch_time)
