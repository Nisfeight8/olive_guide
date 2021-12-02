import requests
import json
import datetime
from django.conf import settings
from django.utils.translation import get_language
from django.template.defaultfilters import date as _date
def getWeather(polygon):
    weather=[]
    API_KEY=settings.OPEN_WEATHER_KEY
    URL = "http://api.openweathermap.org/data/2.5/onecall"
    PARAMS = {'lat':polygon.centroid.y,'lon':polygon.centroid.x,'exclude':'hourly,minutely,alerts','lang':get_language(),'units':'metric','APPID':API_KEY}
    response = requests.get(url = URL, params = PARAMS)
    if response.ok:
        data = response.json()
        for item in data['daily']:
            daily={}
            daily['time']=_date(datetime.datetime.fromtimestamp(item['dt']),"l")
            daily['temp']=item['temp']['day']
            daily['pressure']=item['pressure']
            daily['humidity']=str(item['humidity'])+"%"
            daily['clouds']=str(item['clouds'])+"%"
            daily['wind_speed']=item['wind_speed']
            daily['main']=item['weather'][0]['main']
            daily['description']=item['weather'][0]['description']
            daily['icon']=item['weather'][0]['icon']
            weather.append(daily)
        return weather
