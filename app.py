import streamlit as st
import time
from datetime import datetime
import requests
import os

print("Current Working Directory:", os.getcwd())

# --- Load environment variables safely ---
try:
    from dotenv import load_dotenv

    load_dotenv()
    print(".env loaded")
except Exception as e:
    print(f"dotenv load failed: {e}")

api_key = os.getenv("OPENWEATHER_API_KEY")
print(f"API Key Loaded: {api_key}")


# --- Theme Color Presets ---
theme_colors = {
    "Retro": {"bg": "#1a1a1a", "fg": "#00FF00"},
    "Neon": {"bg": "#000000", "fg": "#FF00FF"},
    "Minimalist": {"bg": "#FFFFFF", "fg": "#000000"},
    "Sunset": {"bg": "#FF4500", "fg": "#FFD700"},
    "Ocean": {"bg": "#001F3F", "fg": "#7FDBFF"},
    "Forest": {"bg": "#013220", "fg": "#A9DFBF"},
    "Cyberpunk": {"bg": "#0D0D0D", "fg": "#39FF14"},
    "Pastel": {"bg": "#FFF0F5", "fg": "#9370DB"},
    "Matrix": {"bg": "#000000", "fg": "#00FF00"},
    "Solarized Dark": {"bg": "#002B36", "fg": "#839496"},
    "Solarized Light": {"bg": "#FDF6E3", "fg": "#657B83"},
    "Monochrome": {"bg": "#2E2E2E", "fg": "#CCCCCC"},
    "Candy": {"bg": "#FF69B4", "fg": "#FFFFFF"},
}

# --- Settings ---
st.set_page_config(
    layout="wide",
    page_title="Digital Clock",
    page_icon="🕒",
    initial_sidebar_state="expanded",
)

# --- Sidebar options ---
format_12h = st.sidebar.checkbox("12-Hour Format (No AM/PM)", value=True)
theme = st.sidebar.selectbox("Theme", list(theme_colors.keys()))
show_date = st.sidebar.checkbox("Show Date", value=True)
show_weather = st.sidebar.checkbox("Show Weather", value=True)
city = st.sidebar.text_input("City for Weather", "Bangalore")

# --- Weather API ---
weather_data = None
if api_key and show_weather:
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(weather_url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            weather_data = f"{city}: {data['main']['temp']} °C, {data['weather'][0]['description'].title()}"
    except:
        weather_data = "Weather data unavailable"
elif not api_key and show_weather:
    weather_data = "API key not set"

# --- CSS for theme and fullscreen ---
colors = theme_colors[theme]
st.markdown(
    f"""
    <style>
    html, body, [class*="css"]  {{
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: {colors['bg']};
        color: {colors['fg']};
    }}
    .clock {{
        font-size: 18vw;
        text-align: center;
        font-weight: bold;
        margin-top: 10vh;
        color: {colors['fg']};
    }}
    .sub {{
        font-size: 4vw;
        text-align: center;
        color: {colors['fg']};
    }}
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", () => {{
            const el = document.documentElement;
            if (el.requestFullscreen) el.requestFullscreen();
        }});
    </script>
""",
    unsafe_allow_html=True,
)

# --- Live Clock Loop ---
placeholder = st.empty()

while True:
    now = datetime.now()
    time_str = now.strftime("%I:%M:%S") if format_12h else now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %d %B %Y")

    with placeholder.container():
        st.markdown(f'<div class="clock">{time_str}</div>', unsafe_allow_html=True)
        if show_date:
            st.markdown(f'<div class="sub">{date_str}</div>', unsafe_allow_html=True)
        if show_weather and weather_data:
            st.markdown(
                f'<div class="sub">{weather_data}</div>', unsafe_allow_html=True
            )

    time.sleep(1)
