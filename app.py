import os
import requests
from flask import Flask, render_template, request

with open('api_key.txt', 'r') as f:
    API_KEY = f.read().strip()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_msg = None
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            error_msg = "Please enter a city name"
        else:
            weather_data = get_weather_data(city)
    return render_template('index.html', weather_data=weather_data, error_msg=error_msg)


def get_weather_data(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon']
            }
            return weather_data
        else:
            return None
    except Exception as e:
        print(e)
        return None


@app.route('/weather/<city>')
def show_weather(city):
    weather_data = get_weather_data(city)
    if weather_data:
        return render_template('weather.html', weather_data=weather_data)
    else:
        return f"Could not retrieve weather data for {city}"


if __name__ == '__main__':
    app.run(debug=True)
