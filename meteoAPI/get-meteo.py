from operator import eq
from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests
import json

url_weather_PZ = 'http://www.meteoam.it/ta/previsione/606/potenza'
content = requests.get(url_weather_PZ, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'})

soup = BeautifulSoup(content.text, 'html.parser')
#get div of today weather
today_weather_div = soup.find("div", {"id": "oggi"})
#get table inside div of today weather
today_weather_table = today_weather_div.find('table')

#get thead with type of information stored in tbody (like: today date, icon of weather, precipitation probability, temperature in °C, humidity, wind(km/h), bursts(km/h))
today_weather_thead = today_weather_table.find('thead')

info_keys = {0: 'Data', 1: 'description', 2: 'precipitation_probability', 3: 'temperature_celsius', 4: 'humidity_percents', 5: 'wind_km_h', 6: 'bursts_km_h'}

today_date = today_weather_thead.find_next('th').get_text()

final_json_dict = {
    "day":"today",
    "date":today_date,
    "hours":[]
}

#get tbody with values for each type of information stored in tbody
today_weather_tbody = today_weather_table.find('tbody')
#get all tr inside tbody, one row for each hour remaining in the day
for tr in today_weather_tbody.findAll('tr'):
    #the first th inside the tr is the hour, get it
    hour = tr.find('th').get_text() #i.e 13:00
    #create a temporary weather object based on specific hour
    tmp_weather_hour = {
        "hour":hour
    }
    #get all td with values
    i = 1; #start from index 1
    for td in tr.findAll('td'):
        if not td.get_text():
            #is the icon case, we need to get image/alt description
            alt_icon_weather = td.find('img')['alt']
            tmp_weather_hour[info_keys[i]] = alt_icon_weather
        else:
            tmp_weather_hour[info_keys[i]] = td.get_text()
        i = i + 1

    #add python object to final json dict
    final_json_dict['hours'].append(tmp_weather_hour)
    

# the result is a JSON string:
final_json = json.dumps(final_json_dict)
print(final_json)

