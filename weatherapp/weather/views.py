from django.shortcuts import render
import requests
from .models import WeatherSearch

# Create your views here.
def weather_view(request):
    weather_data = None
    error_message = None
    history =  WeatherSearch.objects.all().order_by('searched_at')[:5]

    if request.method == 'POST':
        city = request.POST.get('city')
        api_key = "bfb397a022ddd0eac167d8185575a460"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
            }
            WeatherSearch.objects.create(city=city)
        else:
            error_message = "City not found. Please enter a valid city name"

    return render(request, 'weather/weather.html', {
        'weather_data': weather_data, 
        'error_message': error_message, 
        'history': history,
        })






