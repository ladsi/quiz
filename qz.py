import requests
import json
import sqlite3

conn = sqlite3.connect('onecall-weather_owm.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS openweather 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity INTEGER,
            wind_deg INTEGER,
            wind_gust INTEGER 
            )''')

city = "Tbilisi"
key = "a96d6412ce5a268dcbfba2e59b7f9cc5"
lat = 33.44
lon = -94.04
units = "metric"
part = "hourly, daily"
url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={key}&units={units}"

r = requests.get(url)
print(r.status_code)
print(r.headers)
print(r.text)
res = r.json()
#print(json.dumps(res, indent=4))


with open('data.json', 'w') as file:
    json.dump(res, file, indent=4)

print(res['daily'])
print(res['current']['temp'])


for each in res['daily']:
    humidity = each['humidity']
    wind_deg = each['wind_deg']
    wind_gust = each['wind_gust']
    row = (humidity, wind_deg, wind_gust)

    c.execute('INSERT INTO openweather (humidity, wind_deg, wind_gust) VALUES (?, ?, ?)', row)

conn.commit()
conn.close()