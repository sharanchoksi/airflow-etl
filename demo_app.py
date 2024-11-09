import psycopg2
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

# Connect to the Docker-hosted PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",  # Use "localhost" if the port is mapped to the host
        database="postgres",
        user="postgres",
        password="postgres",
        port="5432"    # Replace with the mapped port (e.g., 5432)
    )
    return conn

def fetch_data(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

st.title("Weather Data Dashboard")


query = "SELECT * FROM weather_data LIMIT 100;"  # Fetch more data points if needed
data = fetch_data(query)


headers = ['latitude', 'longitude', 'temperature', 'windspeed', 'winddirection', 'weathercode', 'timestamp']


df = pd.DataFrame(data, columns=headers)


df['timestamp'] = pd.to_datetime(df['timestamp'])


st.write("Data from PostgreSQL:")
st.write(df)

# Plot 1: Temperature Over Time
st.subheader("Temperature Over Time")
fig_temp = px.line(df, x='timestamp', y='temperature', title="Temperature Over Time")
st.plotly_chart(fig_temp)

# Plot 2: Wind Speed Over Time
st.subheader("Wind Speed Over Time")
fig_wind = px.line(df, x='timestamp', y='windspeed', title="Wind Speed Over Time")
st.plotly_chart(fig_wind)

# Plot 3: Wind Direction over Time
st.subheader("Wind Direction over Time")
fig_winddir = px.line(df, x='timestamp', y='winddirection', title="Wind Direction over Time")
st.plotly_chart(fig_winddir)