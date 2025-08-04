import streamlit as st
import time
from datetime import datetime
import requests
import os
from pytz import timezone, all_timezones
from dotenv import load_dotenv

# Load .env
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

# Theme Presets
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

# Streamlit Config
st.set_page_config(
    layout="wide",
    page_title="Wall Clock",
    page_icon="🕒",
    initial_sidebar_state="collapsed",
)

# Sidebar
with st.sidebar:
    st.title("⏱ Settings")
    format_12h = st.checkbox("12-Hour Format", True)
    theme = st.selectbox("Theme", list(theme_colors.keys()))
    show_date = st.checkbox("Show Date", True)
    show_weather = st.checkbox("Show Weather", True)
    city = st.text_input("Weather City", "Bangalore")
    timezone_list = sorted([tz for tz in all_timezones if "/" in tz])
    user_timezone = st.selectbox(
        "Timezone", timezone_list, index=timezone_list.index("Asia/Kolkata")
    )

# Weather API
weather_data = ""
if show_weather and api_key:
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(weather_url, timeout=2)
        if res.ok:
            data = res.json()
            weather_data = (
                f"{data['main']['temp']}°C, {data['weather'][0]['description'].title()}"
            )
        else:
            weather_data = "Weather unavailable"
    except:
        weather_data = "Weather error"

# Theme
colors = theme_colors[theme]

# Inject CSS for fullscreen mobile layout
st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{
        background-color: {colors['bg']};
        color: {colors['fg']};
        height: 100%;
        margin: 0;
        overflow: hidden;
    }}
    .clock {{
        font-size: 20vw;
        font-weight: bold;
        text-align: center;
        color: {colors['fg']};
        margin-top: 10vh;
    }}
    .date {{
        font-size: 6vw;
        text-align: center;
        color: {colors['fg']};
        margin-top: 2vh;
    }}
    .weather {{
        font-size: 5vw;
        text-align: center;
        color: {colors['fg']};
        margin-top: 2vh;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Fullscreen + Prevent Sleep on Mobile (inject JS)
from streamlit.components.v1 import html

html(
    """
<script>
document.addEventListener('click', () => {
    const el = document.documentElement;
    if (el.requestFullscreen) el.requestFullscreen();
});
let noSleep = null;
window.addEventListener('click', function enableNoSleep() {
    if (!noSleep) {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/no-sleep/0.12.0/NoSleep.min.js';
        script.onload = () => {
            noSleep = new NoSleep();
            noSleep.enable();
        };
        document.body.appendChild(script);
    }
}, { once: true });
</script>
""",
    height=0,
)

# Main Loop
placeholder = st.empty()
tz = timezone(user_timezone)

while True:
    now = datetime.now(tz)
    time_str = now.strftime("%I:%M:%S") if format_12h else now.strftime("%H:%M:%S")
    date_str = now.strftime("%A, %d %B %Y")

    with placeholder.container():
        st.markdown(f'<div class="clock">{time_str}</div>', unsafe_allow_html=True)
        if show_date:
            st.markdown(f'<div class="date">{date_str}</div>', unsafe_allow_html=True)
        if show_weather:
            st.markdown(
                f'<div class="weather">{city}: {weather_data}</div>',
                unsafe_allow_html=True,
            )
    time.sleep(1)

st.markdown("---")
st.caption("🔊 Built with ❤️ by Jana using Edge-TTS and Streamlit")