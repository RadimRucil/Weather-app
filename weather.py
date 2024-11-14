import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime

# API klíč a město
API_KEY = "288adbc8c50c90f341e1d369bfb76832"
CITY = "Karviná"

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city + "&lang=cz" + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        description = weather["description"]
        temp = round(main["temp"], 1)
        feels_like = round(main["feels_like"], 1)
        humidity = main["humidity"]
        wind_speed = data["wind"]["speed"]
        
        current_time = datetime.fromtimestamp(data["dt"])
        
        return {
            "description": description,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "time": current_time.strftime("%d.%m.%Y %H:%M:%S")
        }

    else:
        return None

def get_hourly_forecast(api_key, city):
    forecasts = []
    
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city + "&lang=cz" + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        for forecast in data["list"][:6]:
            temp = round(forecast["main"]["temp"], 1)
            feels_like = round(forecast["main"]["feels_like"], 1)
            wind_speed = forecast["wind"]["speed"]
            forecast_time = datetime.fromtimestamp(forecast["dt"])
            
            forecasts.append({
                "time": forecast_time.strftime("%H:%M"),
                "temp": temp,
                "feels_like": feels_like,
                "wind_speed": wind_speed
            })
            
        return forecasts
            
    else:
        return None

def update_weather_label():
    current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    current_time_label.config(text=f"Aktuální čas: {current_datetime}")
    app.after(1000, update_weather_label)

def update_weather():
    weather_data = get_weather(API_KEY, CITY)
    hourly_forecast = get_hourly_forecast(API_KEY, CITY)

    if weather_data is not None and hourly_forecast is not None:
        weather_label.config(text=f"Aktuální počasí v {CITY} ({weather_data['time']}):\n"
                                   f"{weather_data['description']}\n"
                                   f"Teplota: {weather_data['temp']}°C\n"
                                   f"Pocitová teplota: {weather_data['feels_like']}°C\n"
                                   f"Vlhkost: {weather_data['humidity']}%\n"
                                   f"Rychlost větru: {weather_data['wind_speed']} m/s\n"
                                   f"Čas získání dat: {weather_data['time']}")

        forecast_label.config(text="Předpověď na dalších 6 hodin:")
        for forecast in hourly_forecast:
            forecast_label.config(text=forecast_label.cget("text") + f"\n{forecast['time']}: Teplota: {forecast['temp']}°C, Pocitová teplota: {forecast['feels_like']}°C, Rychlost větru: {forecast['wind_speed']} m/s")

app = tk.Tk()
app.title("Aktuální počasí")

weather_label = ttk.Label(app, text="")
weather_label.pack()

forecast_label = ttk.Label(app, text="")
forecast_label.pack()

current_time_label = ttk.Label(app, text="")
current_time_label.pack()

update_button = ttk.Button(app, text="Aktualizovat", command=update_weather)
update_button.pack()

update_weather_label()

app.mainloop()
