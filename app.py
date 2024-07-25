from flask import Flask, render_template
import requests
import geocoder

app = Flask(__name__)

def get_weather_data(latitude, longitude):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"  # Weather API endpoint
    querystring = {"q": f"{latitude},{longitude}"}  # Query using latitude and longitude
    headers = {
        "X-RapidAPI-Key": "28e063f474mshdce606ead0ea727p19c857jsnec0750502031",
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

@app.route('/')
def index():
    # Get latitude and longitude using geocoder
    coordinates = get_current_location()
    if coordinates:
        latitude, longitude = coordinates
        # Get weather data
        weather_data = get_weather_data(latitude, longitude)
        
        if weather_data:
            # Render the HTML template with the weather data
            return render_template('index.html', **weather_data)
    
    return "Failed to retrieve weather data."

def get_current_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.latlng
    else:
        return None

if __name__ == "__main__":
    app.run(debug=True)
