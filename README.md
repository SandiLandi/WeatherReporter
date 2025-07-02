# 🌦️ WeatherReporter — PDF Weather Forecast App

This Python application fetches real-time weather data using **OpenWeatherMap** and **Weatherstack** APIs, compares results, and generates professional **PDF weather reports**.

---

## 📌 Features

- 📍 Auto-location detection via `ipinfo.io`
- 🔁 Dual API support: **OpenWeatherMap** and **Weatherstack**
- 📑 PDF report generation with:
  - **Today’s weather comparison**
  - **5-day / 3-hour forecast**
- 🌐 Weather icons included in PDF
- 🖋️ DejaVu font embedding
- 🛡️ SSL verification disabled for quick debugging (not for production)

---

## 📂 Files Overview

| File                     | Description                               |
|--------------------------|-------------------------------------------|
| `Meto 0.9.py`            | Initial working version with full logic   |
| `Meto 1.0.py`            | Improved, modular structure               |
| `weayher_FORECADT.py`    | Focuses only on 5-day forecast generation |
| `fonts/DejaVuSans.ttf`   | Custom font embedded in PDF               |
| `certs/cacert.pem`       | Optional certificate file (unused now)    |

---

## 📦 Requirements

Install with pip:


pip install requests reportlab urllib3
🔧 Usage
bash
Копировать
Редактировать
python "Meto 1.0.py"
Follow prompts in console to select:

📍 City (auto or manual)

⏱️ Forecast duration (t = today / f = 5 days)

A PDF will be saved like:

weather_report_combined_Warsaw.pdf

weather_forecast_Warsaw.pdf

🔐 API Keys
You’ll need your own API keys:

OpenWeatherMap

Weatherstack

Insert them into the script:

python
Копировать
Редактировать
key_openweathermap = 'your_openweather_key'
key_weatherstack = 'your_weatherstack_key'
🧠 Notes
Font registration uses fonts/DejaVuSans.ttf

Icons from OpenWeatherMap & Weatherstack are embedded into PDFs

SSL verification disabled (verify=False) for convenience only!


👨‍💻 Author
Created by SandiLandi
