from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from main.forms import CityWeather
import requests


# Create your views here.

def get_lat_lon(city):
    KEY = "373814d521bdbdc5b3a01d47ac72ae49"
    URL = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={KEY}"
    data = requests.get(URL)
    if data.status_code == 200:
        data = data.json()
        lat = data[0]['lat']
        lon = data[0]['lon']

        URL2 = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={KEY}"
        data2 = requests.get(URL2)
        data2 = data2.json()
        print(data2)

        temp = round(data2['main']['temp'] - 272.15, 1)
        feels = round(data2['main']['feels_like'] - 272.15, 1)
        pressure = data2['main']['pressure']
        humidity = data2['main']['humidity']
        wind = data2['wind']['speed']
        desc = data2['weather'][0]['main']
        icon = data2['weather'][0]['icon']
        print(desc)
        return lat, lon, temp, feels, pressure, wind, desc, icon, humidity
    else:
        raise OSError

def weather(response):
    if response.method == "POST":
        form = CityWeather(response.POST)

        if form.is_valid():
            city = form.cleaned_data['city']
            
            try:
                lat, lon, temp, feels, pressure, wind, desc, icon, humidity = get_lat_lon(city)

            except OSError as er:
                print(f"An error occured {er}, bad status_code")

            context = {"city":city,
                        "temp":temp,
                        "feels": feels,
                        "pressure": pressure,
                        "wind":wind,
                        "form": form,
                       "desc": desc,
                       "icon": icon,
                       "humidity": humidity
                       }

            print(context)

            return render(response, 'main/content.html', context)
    else:
        form = CityWeather()

    return render(response, "main/base.html", {"form":form})

def home(response):
    return render(response, 'main/base.html', {})