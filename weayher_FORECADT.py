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


def get_weather_forecast(api_key, city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"

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


def create_pdf_report_forecast(data):
    city = data['city']['name']
    pdf_file = f"weather_forecast_{city}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Регистрация шрифта DejaVuSans
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVuSans.ttf'))
    c.setFont('DejaVuSans', 12)

    # Добавление заголовка
    c.setFont('DejaVuSans', 16)
    c.drawString(40, height - 40, f"Weather Forecast for {city}")
    c.setFont('DejaVuSans', 12)
    y = height - 60

    # Прогноз на ближайшие 5 дней с интервалом в 3 часа
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
            c.setFont('DejaVuSans', 12)
            y = height - 40

    c.showPage()
    c.save()
    print(f"PDF report created successfully: {pdf_file}")
    return pdf_file


def get_location():
    try:
        # Отправляем запрос к ipinfo.io для получения информации о местоположении
        response = requests.get('https://ipinfo.io', verify=False)
        response.raise_for_status()
        data = response.json()

        # Извлекаем информацию о местоположении
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
    key_openweathermap = "YOUR_API_KEY_HERE"  # Замените на ваш действительный API ключ

    country, city = get_location()
    print(f"Detected location: {country}, {city}")

    # Спрашиваем у пользователя, хочет ли он использовать автоматически определенное местоположение
    use_detected_location = input(f"Do you want to check the weather in {city}, {country}? (yes/no): ").strip().lower()

    if use_detected_location != 'yes':
        city = input("Enter the city name: ").strip()

    weather_forecast_data = get_weather_forecast(key_openweathermap, city)

    if weather_forecast_data:  # Проверяем, что данные о погоде получены успешно
        pdf_file = create_pdf_report_forecast(weather_forecast_data)
        print(f"Report saved to: {pdf_file}")

