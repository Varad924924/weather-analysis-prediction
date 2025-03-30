import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# OpenWeatherMap API Key (Replace with your own)
API_KEY = "887b9acf1f212366e3d79983791be7e8"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# List of Cities
cities = [ # Konkan Division
    "Alibag", "Ambernath", "Andheri", "Borivali", "Bhiwandi", "Dahanu", "Guhagar", "Jawhar", "Kalyan", "Karjat",
    "Khalapur", "Kurla", "Lanja", "Mahad", "Mangaon", "Mazgaon", "Mhasla", "Mokhada", "Mumbai City", "Mumbai Suburban",
    "Murbad", "Murud", "Panvel", "Palghar", "Pen", "Poladpur", "Raigad", "Rajapur", "Ratnagiri", "Roha", "Sawantwadi",
    "Shahapur", "Shrivardhan", "Sindhudurg", "Sudhagad", "Talasari", "Thane", "Uran", "Ulhasnagar", "Vasai", "Velhe",
    "Vikramgad", "Wada",
    
    # Pune Division
    "Akkalkot", "Baramati", "Bhor", "Chandgad", "Daund", "Gadhinglaj", "Haveli", "Hatkanangale", "Indapur", "Jaoli",
    "Jat", "Kagal", "Karmala", "Karad", "Khandala", "Khatav", "Kolhapur", "Koregaon", "Lanja", "Malshiras", "Mangalvedha",
    "Man", "Miraj", "Mulshi", "Murbad", "Pandharpur", "Panhala", "Patan", "Phaltan", "Pimpri-Chinchwad", "Pune",
    "Purandar", "Sangli", "Sangola", "Satara", "Shirol", "Shirala", "Shirur", "Solapur", "Tasgaon", "Wai", "Walwa",

    # Nashik Division
    "Ahmednagar", "Akole", "Baglan", "Chalisgaon", "Chandwad", "Deola", "Dindori", "Dhule", "Igatpuri", "Jalgaon",
    "Jamkhed", "Junnar", "Kalwan", "Malegaon", "Manmad", "Nandurbar", "Nashik", "Niphad", "Parner", "Pathardi",
    "Rahata", "Rahuri", "Raver", "Sakri", "Satana", "Shahada", "Shevgaon", "Shrigonda", "Sinnar", "Taloda", "Trimbak",
    "Yeola",

    # Aurangabad Division
    "Aurangabad (Chhatrapati Sambhajinagar)", "Ambad", "Ashti", "Badnapur", "Beed", "Bhokardan", "Chhatrapati Sambhajinagar",
    "Dharashiv", "Gangapur", "Jafrabad", "Jalna", "Kaij", "Kannad", "Latur", "Majalgaon", "Mantha", "Nanded", "Osmanabad",
    "Parbhani", "Paithan", "Partur", "Parli", "Phulambri", "Sillod", "Tuljapur", "Udgir", "Vaijapur", "Washi", "Wadwani",

    # Amravati Division
    "Achalpur", "Akola", "Amravati", "Anjangaon", "Arni", "Balapur", "Bhatkuli", "Buldhana", "Chandur Bazar", 
    "Chandur Railway", "Chikhli", "Daryapur", "Deulgaon Raja", "Digras", "Ghatanji", "Jalgaon Jamod", "Khamgaon",
    "Karanja", "Lonar", "Malkapur", "Manora", "Mangrulpir", "Mehkar", "Motala", "Murtizapur", "Nandgaon Khandeshwar",
    "Patur", "Ralegaon", "Risod", "Teosa", "Tiwasa", "Umarkhed", "Warud", "Washim", "Yavatmal",

    # Nagpur Division
    "Arjuni Morgaon", "Ashti", "Ballarpur", "Bhandara", "Bhadravati", "Bhiwapur", "Brahmapuri", "Chandrapur", 
    "Chamorshi", "Chimur", "Deori", "Desaiganj", "Gadchiroli", "Gondia", "Gondpipri", "Hingna", "Kamptee", 
    "Katol", "Kuhi", "Lakhandur", "Lakhani", "Mauda", "Mohadi", "Mul", "Nagbhid", "Nagpur", "Nagpur City", 
    "Nagpur Rural", "Narkhed", "Parseoni", "Pombhurna", "Rajura", "Ramtek", "Sadak Arjuni", "Salekasa", 
    "Sawali", "Savner", "Seloo", "Tiroda", "Tumsar", "Umred", "Warora"]

# Streamlit UI
st.title("🌤️ Weather Dashboard")

# City Selection
city = st.selectbox("Select a City", cities)

# Date Picker for Historical Trends
selected_date = st.date_input("Select a Date", datetime.today())

# Fetch Weather Data
params = {"q": city, "appid": API_KEY, "units": "metric"}
response = requests.get(BASE_URL, params=params)
data = response.json()

if "list" in data:
    weather_data = []
    for entry in data["list"]:
        timestamp = datetime.utcfromtimestamp(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]
        desc = entry["weather"][0]["description"]
        weather_data.append([timestamp, temp, humidity, wind_speed, desc])

    # Convert to DataFrame
    df = pd.DataFrame(weather_data, columns=["Timestamp", "Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Weather Description"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # Filter by Selected Date
    df_filtered = df[df["Timestamp"].dt.date == selected_date]

    # Display Data
    st.subheader(f"Weather Forecast for {city} on {selected_date}")
    st.dataframe(df_filtered)

    # Visualization
    st.subheader("📊 Temperature Trends")
    fig_temp = px.line(df_filtered, x="Timestamp", y="Temperature (°C)", title="Temperature Over Time", markers=True)
    st.plotly_chart(fig_temp)
    
    st.subheader("💨 Wind Speed Trends")
    fig_wind = px.line(df_filtered, x="Timestamp", y="Wind Speed (m/s)", title="Wind Speed Over Time", markers=True)
    st.plotly_chart(fig_wind)
    
    st.subheader("💦 Humidity Trends")
    fig_humidity = px.line(df_filtered, x="Timestamp", y="Humidity (%)", title="Humidity Over Time", markers=True)
    st.plotly_chart(fig_humidity)

    st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #FFBF00;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }
        .footer a {
            color: #0073b1;
            text-decoration: none;
            font-weight: bold;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        Created by <a href="https://www.linkedin.com/in/varad-gorhe-719ab21b6/" target="_blank">Varad Gorhe</a> <br>
        follow me on <br>
         <a href="https://www.linkedin.com/in/varad-gorhe-719ab21b6/" target="_blank">linkedin</a> <br>
        <a href="https://wa.me/qr/22ZEFUXERUTIP1" target="_blank">Whatsapp</a> <br>
        <a href="https://www.instagram.com/varadgorhe924?igsh=Nng0eGFrbThiODdi" target="_blank">Instagram</a> <br>
                
    </div>
""", unsafe_allow_html=True)

else:
    st.error("Failed to fetch weather data. Please try again.")
