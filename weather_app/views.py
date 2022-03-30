import re
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import requests
from .models import City
from .forms import AddCityForm


def home(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=69643db8c08fc089ab6dd8f6a1a9b4cd"

    if request.method == 'POST':
        if 'add_form' in request.POST:
            form = AddCityForm(data = request.POST)
            form.save()
            return HttpResponseRedirect(reverse("home"))
        elif 'del_form' in request.POST:
            city_names_string = request.POST['name']
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
        r = requests.get(url.format(city)).json()
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

    context = {"weather_data" : weather_data, 
    'add_city_form' : add_city_form
    }
    return render(request, 'weather_app/home.html', context)
