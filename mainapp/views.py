from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.


def index(request):
    cities = City.objects.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=d6508e4dc5bc577bc633ea0ac04c4ff3'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
            'humidity' : city_weather['main']['humidity'],
            'pressure' : city_weather['main']['pressure'],
            'windspeed' : city_weather['wind']['speed']
        }

        weather_data.append(weather)
    
    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'index.html', context)