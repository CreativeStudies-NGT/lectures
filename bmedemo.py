import datetime
import pandas as pd
import sqlite3
import random

temperature = random.gauss(mu=26.0, sigma=2.0)
humidity = random.gauss(mu=66.0, sigma=12.0)
pressure = random.gauss(mu=1010.0, sigma=8.0)

print(f'temperature: {temperature:.1f} humidity: {humidity:.1f} pressure: {pressure:.1f}')

# Connecting to Database to record sensor data
db_name = 'bme280_record.db'
table_name = 'data'
conn = sqlite3.connect(db_name)
c = conn.cursor()

# テーブルが無ければ作成（あれば何もしない）
CREATE_TABLE = (
    'CREATE TABLE IF NOT EXISTS ' + table_name +
    '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
    'date TEXT, '
    'temperature REAL, '
    'humidity REAL, '
    'pressure REAL)')
c.execute(CREATE_TABLE)

# Save data to a table in the DB
sqlstr = (
    'INSERT INTO ' + table_name +
    ' ("date", "temperature", "humidity", "pressure") VALUES(?, ?, ?, ?)')
date = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
c.execute(sqlstr, [date, temperature, humidity, pressure])
conn.commit()

# dbをpandasで読み出す
df = pd.read_sql('SELECT * FROM ' + table_name, conn)

# Closing DB
c.close()
conn.close()

# Display data as a DataFrame
df.tail()
