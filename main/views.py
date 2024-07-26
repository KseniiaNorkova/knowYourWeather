from django.shortcuts import render
import requests

from .models import City
from .token import TOKEN
from .forms import CityForm


def index(request):
    app_id = TOKEN
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=' + app_id + '&units=metric'
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()
    
    cities = City.objects.all()
    all_cities = []

    for city in cities:   
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name.title(),
            'temp': int(res['main']['temp']),
                    }
        if not city_info in all_cities:
            all_cities.insert(0, city_info)
        if len(all_cities) > 3:
            all_cities.pop(-1)
    
    context = {       
        'title': 'Know Your Weather',
        'content': 'Start Your Search',
        'all_info': all_cities,
        'form': form,
    }

    return render(request, 'main/index.html', context)

