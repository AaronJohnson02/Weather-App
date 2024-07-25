from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather_data(latitude, longitude):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"  # Weather API endpoint
    querystring = {"q": f"{latitude},{longitude}"}  # Query using latitude and longitude
    headers = {
        "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()

        # Extract relevant data from API response
        city_name = data['location']['name']
        icon_url = 'https:' + data['current']['condition']['icon']
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        description = data['current']['condition']['text']
        wind = data['current']['wind_kph']
        pressure = data['current']['pressure_mb']
        pl = data['current']['precip_mm']
        return {
            'city_name': city_name,
            'icon': icon_url,
            'temp': temp,
            'humidity': humidity,
            'description': description,
            'wind': wind,
            'pressure': pressure,
            'precipitation_level': pl
        }
    else:
        return None

@app.route('/', methods=['GET'])
def index():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if latitude and longitude:
        weather_data = get_weather_data(latitude, longitude)
        
        if weather_data:
            return render_template('index.html', **weather_data)
        else:
            return "Failed to retrieve weather data."
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
