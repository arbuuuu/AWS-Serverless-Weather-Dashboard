import json
import urllib3
import os 
from collections import defaultdict

# Get the API key from the function's Environment Variables
API_KEY = os.environ.get('API_KEY', '')     // put your API key in ''

http = urllib3.PoolManager()

# --- NEW HELPER FUNCTION ---
def convert_degrees_to_direction(degrees):
    # Ek simple function jo degrees ko compass direction mein badalta hai
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    # Har direction 22.5 degrees ka hota hai (360 / 16)
    try:
        index = round(degrees / (360. / len(directions))) % len(directions)
        return directions[index]
    except Exception as e:
        print(f"Error converting degrees: {e}")
        return "N/A" # Error ke case mein
# --- END NEW FUNCTION ---

def lambda_handler(event, context):
    
    # --- 1. Get the city from the API Gateway ---
    try:
        city = event['queryStringParameters']['city']
        if not city:
            raise KeyError
            
    except (KeyError, TypeError):
        print("Missing 'city' query parameter")
        return {
            'statusCode': 400,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'message': "Missing 'city' query parameter. Please provide a city."})
        }

    # --- 2. Fetch Weather Data (5-day forecast) ---
    print(f"Fetching 5-day forecast for: {city}")
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    
    try:
        r = http.request('GET', url)
        data = json.loads(r.data.decode('utf-8'))
        
        if r.status != 200:
            print(f"OpenWeather API Error: {data}")
            return {
                'statusCode': r.status,
                'headers': { 'Access-Control-Allow-Origin': '*' },
                'body': json.dumps(data) 
            }

    except Exception as e:
        print(f"Error fetching data: {e}")
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'message': 'Internal server error while fetching weather.'})
        }
    
    # --- 3. Process the 5-Day Forecast Data (Smartly!) ---
    daily_data = defaultdict(list)
    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        daily_data[date].append(item)

    daily_forecasts = []
    sorted_dates = sorted(daily_data.keys())
    
    for date in sorted_dates:
        items_for_day = daily_data[date]
        temp_min = min(item['main']['temp_min'] for item in items_for_day)
        temp_max = max(item['main']['temp_max'] for item in items_for_day)
        midday_item = items_for_day[len(items_for_day) // 2]
        
        daily_forecasts.append({
            'dt_txt': midday_item['dt_txt'],
            'temp_min': temp_min,
            'temp_max': temp_max,
            'icon': midday_item['weather'][0]['icon'],
            'description': midday_item['weather'][0]['description']
        })

    # --- 4. Build a clean response object ---
    
    # Get current weather
    current_weather = data['list'][0]
    
    # --- NEW: Add wind direction to the 'current' object ---
    wind_degrees = current_weather['wind'].get('deg', 0)
    current_weather['wind_direction'] = convert_degrees_to_direction(wind_degrees)
    # --- END NEW ---
    
    response_body = {
        "city": data['city'],
        "current": current_weather, # Ab ismein 'wind_direction' bhi hai
        "forecast": daily_forecasts
    }
    
    print(f"Successfully processed data for {city}")
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response_body)
    }
