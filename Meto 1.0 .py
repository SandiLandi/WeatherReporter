import requests
import urllib3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
import datetime

# Отключаем предупреждения о проверке сертификатов
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Константы
FONT_NAME = 'DejaVuSans'
FONT_PATH = 'fonts/DejaVuSans.ttf'
API_URL_WEATHER_OPENWEATHERMAP = "https://api.openweathermap.org/data/2.5/weather"
API_URL_FORECAST_OPENWEATHERMAP = "https://api.openweathermap.org/data/2.5/forecast"
API_URL_WEATHERSTACK = "http://api.weatherstack.com/current"

PERIOD_OPTIONS = {
    't': 'today',
    'f': 'five days'
}

def register_fonts():
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

def get_weather_openweathermap(api_key, city):
    try:
        res = requests.get(
            API_URL_WEATHER_OPENWEATHERMAP,
            params={'q': city, 'units': 'metric', 'lang': 'en', 'APPID': api_key},
            verify=False
        )
        res.raise_for_status()
        data = res.json()
        if data.get('cod') != 200:
            print("Error in API request:", data.get('message', 'Unknown error'))
            return None
        weather_data_openweathermap = {
            "City": city,
            "Weather": data['weather'][0]['description'],
            "Temperature": data['main'].get('temp', 'No temperature data'),
            "Humidity": data['main'].get('humidity', 'No humidity data'),
            "Pressure": data['main'].get('pressure', 'No pressure data'),
            "Wind Speed": data['wind'].get('speed', 'No wind speed data'),
            "Wind Direction": data['wind'].get('deg', 'No wind direction data'),
            "Wind Gust": data['wind'].get('gust', 'No gust data'),
            "Weather Icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "Max Temp": data['main'].get('temp_max', 'No max temp data'),
            "Min Temp": data['main'].get('temp_min', 'No min temp data')
        }
        print(weather_data_openweathermap)
        return weather_data_openweathermap
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None

def get_weather_weatherstack(api_key, city):
    try:
        res = requests.get(
            API_URL_WEATHERSTACK,
            params={'access_key': api_key, 'query': city}
        )
        res.raise_for_status()
        data = res.json()
        if 'error' in data:
            print("Error in API request:", data['error']['info'])
            return None
        weather_data_weatherstack = {
            "City": data['location'].get('name', 'Unknown City'),
            "Weather": data['current'].get('weather_descriptions', ['No description'])[0],
            "Temperature": data['current'].get('temperature', 'No temperature data'),
            "Humidity": data['current'].get('humidity', 'No humidity data'),
            "Pressure": data['current'].get('pressure', 'No pressure data'),
            "Wind Speed": data['current'].get('wind_speed', 'No wind speed data'),
            "Wind Direction": data['current'].get('wind_degree', 'No wind direction data'),
            "Wind Gust": data['current'].get('wind_gust', 'No gust data'),
            "Weather Icon": data['current'].get('weather_icons', [''])[0],
            "Max Temp": data['current'].get('temp_max', 'No max temp data'),
            "Min Temp": data['current'].get('temp_min', 'No min temp data')
        }
        print(weather_data_weatherstack)
        return weather_data_weatherstack
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None

def get_weather_forecast(api_key, city):
    try:
        url = f"{API_URL_FORECAST_OPENWEATHERMAP}?q={city}&units=metric&appid={api_key}"
        res = requests.get(url, verify=False)
        res.raise_for_status()
        weather_forecast_data = res.json()
        return weather_forecast_data
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        print("Response content:", errh.response.content)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return None

def create_combined_pdf_report(data_openweathermap, data_weatherstack):
    register_fonts()
    city = data_openweathermap["City"]
    pdf_file = f"weather_report_combined_{city}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    c.setFont(FONT_NAME, 12)
    c.setFont(FONT_NAME, 16)
    c.drawString(40, height - 40, "Weather Report Comparison")
    c.setFont(FONT_NAME, 12)
    y = height - 60
    c.drawString(40, y, "OpenWeatherMap")
    c.drawString(width / 2 + 20, y, "Weatherstack")
    y -= 20
    keys = ["Weather", "Temperature", "Humidity", "Pressure", "Wind Speed", "Wind Direction", "Wind Gust", "Max Temp", "Min Temp"]
    for key in keys:
        c.drawString(40, y, f"{key}: {data_openweathermap.get(key, 'N/A')}")
        c.drawString(width / 2 + 20, y, f"{key}: {data_weatherstack.get(key, 'N/A')}")
        y -= 20
    insert_weather_icon(c, data_openweathermap["Weather Icon"], 40, y)
    insert_weather_icon(c, data_weatherstack["Weather Icon"], width / 2 + 20, y)
    c.showPage()
    c.save()
    print(f"PDF report created successfully: {pdf_file}")
    return pdf_file

def insert_weather_icon(canvas_obj, icon_url, x, y):
    if icon_url:
        try:
            img = ImageReader(icon_url)
            canvas_obj.drawImage(img, x, y - 100, width=50, height=50)
        except Exception as e:
            print(f"Failed to load image: {e}")

def create_pdf_report_forecast(data):
    register_fonts()
    city = data['city']['name']
    pdf_file = f"weather_forecast_{city}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    c.setFont(FONT_NAME, 12)
    c.setFont(FONT_NAME, 16)
    c.drawString(40, height - 40, f"Weather Forecast for {city}")
    c.setFont(FONT_NAME, 12)
    y = height - 60
    c.drawString(40, y, "5 Day / 3 Hour Forecast:")
    y -= 20
    for forecast in data['list']:
        dt = datetime.datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M')
        temp = forecast['main']['temp']
        weather = forecast['weather'][0]['description']
        c.drawString(40, y, f"{dt}: Temp: {temp}C, Weather: {weather}")
        y -= 20
        if y < 40:
            c.showPage()
            c.setFont(FONT_NAME, 12)
            y = height - 40
    c.showPage()
    c.save()
    print(f"PDF report created successfully: {pdf_file}")
    return pdf_file

def get_location():
    try:
        response = requests.get('https://ipinfo.io', verify=False)
        response.raise_for_status()
        data = response.json()
        country = data.get('country', 'Unknown Country')
        city = data.get('city', 'Unknown City')
        return country, city
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
        return 'Unknown Country', 'Unknown City'

if __name__ == "__main__":
    key_openweathermap = 'fe0e1148854f92b415e000b0db8b4e12'
    key_weatherstack = '53ac2a535062a0c262501d02b5102343'
    country, city = get_location()
    print(f"Detected location: {country}, {city}")
    use_detected_location = input(f"Do you want to check the weather in {city}, {country}? (yes/no): ").strip().lower()
    if use_detected_location != 'yes':
        city = input("Enter the city name: ").strip()
    weather_period_input = input("Do you want to check the weather for today or five days? (t/f): ").strip().lower()
    weather_period = PERIOD_OPTIONS.get(weather_period_input)
    if not weather_period:
        print("Invalid input. Please enter 't' for today or 'f' for five days.")
    elif weather_period == 'today':
        weather_data_openweathermap = get_weather_openweathermap(key_openweathermap, city)
        weather_data_weatherstack = get_weather_weatherstack(key_weatherstack, city)
        if weather_data_openweathermap and weather_data_weatherstack:
            pdf_file = create_combined_pdf_report(weather_data_openweathermap, weather_data_weatherstack)
            print(f"Report saved to: {pdf_file}")
    else:
        weather_forecast_data = get_weather_forecast(key_openweathermap, city)
        if weather_forecast_data:
            pdf_file = create_pdf_report_forecast(weather_forecast_data)
            print(f"Report saved to: {pdf_file}")
