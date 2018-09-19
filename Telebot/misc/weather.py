import requests
import json

API_KEY = "196eececc4ac648bb8ec3cd0d7679d7e"

CITY = "Kiev"
COUNTRY_CODE = "UA"
LINK = "http://api.openweathermap.org/data/2.5/weather?q={0},{1}&units=metric&APPID={2}".format(CITY, COUNTRY_CODE, API_KEY)

def get_weather():
    r = requests.get(LINK)
    jr = json.loads(r.text)
    print(jr['weather'][0]['description'])
    formated = "Weather in {0}, {1}: {2}, temprature - {3}*C, humidity - {4}%, wind - {5} meters/sec.".format(jr['name'], jr['sys']['country'], jr['weather'][0]['description'], jr['main']['temp'], jr['main']['humidity'], jr['wind']['speed'])

    return formated
