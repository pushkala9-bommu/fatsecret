import json
import requests
import schedule
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import streamlit as st
api="a7d757bf2e0bc71e57a9661e6b9ea93e"
baseURL="https://api.openweathermap.org/data/2.5/weather?q="
city=input("enter the name of the city:")
completeURL=baseURL+city+"&appid="+api
response=requests.get(completeURL)
data=response.json()
print("temperature",(data)["main"]["temp"])
print("temperature feels_like",(data)["main"]["feels_like"])
print("minimum temperature",(data)["main"]["temp_min"])
print("maximum temperature",(data)["main"]["temp_max"])
print("humidity",(data)["main"]["humidity"])

def store_data(data, filename="weather_data.csv"):
    df = pd.DataFrame([data])
    if not pd.io.common.file_exists(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

# Function to plot temperature trends
def plot_temperature(filename="weather_data.csv"):
    df = pd.read_csv(filename)
    df['Time'] = pd.to_datetime(df['Time'])
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Temperature (C)'], marker='o')
    plt.title('Temperature Trend')
    plt.xlabel('Time')
    plt.ylabel('Temperature (C)')
    plt.grid(True)
    plt.show()

# Function to display dashboard using Streamlit
def display_dashboard():
    st.title("Live Weather Dashboard")
    city = st.text_input("Enter city name", CITY)
    if st.button("Fetch Weather"):
        weather_info = fetch_weather(city)
        if weather_info:
            st.write(weather_info)
            store_data(weather_info)

    if st.button("Show Temperature Trend"):
        plot_temperature()

# Schedule the data fetch every hour
schedule.every(1).hour.do(lambda: store_data(fetch_weather(CITY)))

if __name__ == "__main__":
    display_dashboard()

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)



