import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests

from weather_app.constants import WEATHER_API_KEY
from weather_app.models import City
from weather_app.forms import AddCityForm


def home(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

    if request.method == 'POST':
        if 'add_form' in request.POST:
            data = request.POST
            if ("," in data["name"]):
                print("multiple entries found")
                return HttpResponseRedirect(reverse("home"))
            else:
                form = AddCityForm(data)
                form.save()
                return HttpResponseRedirect(reverse("home"))
        elif 'del_form' in request.POST:
            city_names_string = request.POST['name']
            original_to_delete = City.objects.filter(name=city_names_string)
            if original_to_delete.exists():
                original_to_delete.delete()
            city_names_list = city_names_string.split(",")
            for city in city_names_list:
                city_to_delete = City.objects.filter(name=city)
                if city_to_delete.exists():
                    city_to_delete.delete()
            return HttpResponseRedirect(reverse("home"))
        else:
            pass
    else:
        add_city_form = AddCityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        resp = requests.get(url.format(city, WEATHER_API_KEY))
        if resp.status_code == 200:
            r = resp.json()
            # data
            temperature = round(float(r["main"]["temp"]) - 273.15, 2) # in celsius
            feels_like = round(float(r["main"]["feels_like"]) - 273.15, 2)
            humidity = round(float(r["main"]["humidity"]),2) # in %
            wind_speed = r["wind"]["speed"] # in m/s
            description = r["weather"][0]["description"]
            icon = r["weather"][0]["icon"]

            city_weather = {
                "city": city,
                "temperature": temperature,
                "feels_like" : feels_like,
                "humidity" : humidity,
                "wind_speed" : wind_speed,
                "description": description,
                "icon": icon
            }

            weather_data.append(city_weather)
        else:
            continue

    context = {
        "weather_data" : weather_data, 
        'add_city_form' : add_city_form
    }
    return render(request, 'weather_app/home.html', context)