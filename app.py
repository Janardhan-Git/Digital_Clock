import streamlit as st
import time
from datetime import datetime
import requests

# --- Settings ---
st.set_page_config(layout="wide", page_title="Digital Clock", initial_sidebar_state="expanded")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        margin: 0;
        padding: 0;
        overflow: hidden;
        background-color: black;
        color: white;
    }
    .clock {
        font-size: 18vw;
        text-align: center;
        font-weight: bold;
        margin-top: 10vh;
    }
    .sub {
        font-size: 4vw;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar options ---
format_12h = st.sidebar.checkbox("12-Hour Format", value=True)

# Theme presets
theme = st.sidebar.selectbox("Theme", ["Retro", "Neon", "Minimalist"])
theme_colors = {
    "Retro": {"bg": "#1a1a1a", "fg": "#00FF00"},
    "Neon": {"bg": "#000000", "fg": "#FF00FF"},
    "Minimalist": {"bg": "#FFFFFF", "fg": "#000000"},
}

# Weather API
city = st.sidebar.text_input("City for Weather", "Bangalore")
weather_data = None
api_key = "your_openweathermap_api_key"  # Replace with your key

try:
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(weather_url, timeout=2)
    if response.status_code == 200:
        data = response.json()
        weather_data = f"{city}: {data['main']['temp']} °C, {data['weather'][0]['description'].title()}"
except:
    weather_data = "Weather data unavailable"

# Apply theme
colors = theme_colors[theme]
st.markdown(f"""
    <style>
    body {{
        background-color: {colors['bg']};
        color: {colors['fg']};
    }}
    .clock {{
        color: {colors['fg']};
    }}
    .sub {{
        color: {colors['fg']};
    }}
    </style>
""", unsafe_allow_html=True)

# --- Live Clock Loop ---
placeholder = st.empty()

while True:
    now = datetime.now()
    if format_12h:
        time_str = now.strftime("%I:%M:%S %p")
    else:
        time_str = now.strftime("%H:%M:%S")

    date_str = now.strftime("%A, %d %B %Y")

    with placeholder.container():
        st.markdown(f'<div class="clock">{time_str}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sub">{date_str}</div>', unsafe_allow_html=True)
        if weather_data:
            st.markdown(f'<div class="sub">{weather_data}</div>', unsafe_allow_html=True)

    time.sleep(1)
