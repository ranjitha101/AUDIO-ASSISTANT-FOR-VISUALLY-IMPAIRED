import requests
def get_weather(city="Mangalore"):
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        return f"The weather in {city} is {weather} with temperature {temp}°C."
    else:
        return "Unable to fetch weather data."
