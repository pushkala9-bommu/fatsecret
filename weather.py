import requests

def get_weather(api_key, city):
    # OpenWeatherMap API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?q={"london"}&appid={"a7d757bf2e0bc71e57a9661e6b9ea93e"}&units=metric"
    
    try:
        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        weather_data = response.json()
        
        # Extract relevant information
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_description = weather_data['weather'][0]['description']
        
        # Print the weather information
        print(f"Weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Conditions: {weather_description}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")

if __name__ == "__main__":
    # Replace 'your_api_key_here' with your actual OpenWeatherMap API key
    api_key = "a7d757bf2e0bc71e57a9661e6b9ea93e"
    
    # Replace 'London' with the city you want to check the weather for
    city = "London"
    
    get_weather(api_key, city)