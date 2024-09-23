import streamlit as st
import pyowm
from pyowm.utils import timestamps
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
import numpy as np

# Initialize OpenWeatherMap API with your API key
owm = pyowm.OWM('7dfb5792c218daad8e2a74a8473cbf3a')
mgr = owm.weather_manager()

# Streamlit frontend setup
st.title("🌥️ Day Weather Forecast 🌤️")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")

# Input for the city name
place = st.text_input("NAME OF THE CITY:", "")

if not place:
    st.write("Input a CITY!")

# Selection for temperature unit
unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))

# Selection for graph type
g_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if place:
    # Retrieve the 5 day / 3 hour forecast data
    try:
        forecast = mgr.forecast_at_place(place, '3h').forecast

        # Process weather data
        temps_by_day = defaultdict(lambda: {"max": float('-inf'), "min": float('inf')})

        for weather in forecast:
            date = datetime.datetime.fromtimestamp(weather.reference_time()).date()
            if unit == "Celsius":
                temp = weather.temperature('celsius')['temp']
            else:
                temp = weather.temperature('fahrenheit')['temp']
            temps_by_day[date]["max"] = max(temp, temps_by_day[date]["max"])
            temps_by_day[date]["min"] = min(temp, temps_by_day[date]["min"])

        dates = list(temps_by_day.keys())
        max_temps = [temps["max"] for temps in temps_by_day.values()]
        min_temps = [temps["min"] for temps in temps_by_day.values()]

        # Plotting the forecast using Matplotlib
        plt.figure(figsize=(10, 5))

        if g_type == "Line Graph":
            plt.plot(dates, max_temps, marker='o', color='red', label='Max Temp')
            plt.plot(dates, min_temps, marker='o', color='blue', label='Min Temp')
            plt.xlabel('Date')
            plt.ylabel(f'Temperature (°{unit[0]})')
            plt.title(f"{place} - 5 Day Weather Forecast")
            plt.xticks(rotation=45)
            plt.legend()

        elif g_type == "Bar Graph":
            x = np.arange(len(dates))  # the label locations
            width = 0.35  # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(x - width/2, min_temps, width, label='Min Temp')
            rects2 = ax.bar(x + width/2, max_temps, width, label='Max Temp')

            # Add some text for labels, title and custom x-axis tick labels, etc.
            ax.set_ylabel(f'Temperature (°{unit[0]})')
            ax.set_title(f"{place} - 5 Day Weather Forecast")
            ax.set_xticks(x)
            ax.set_xticklabels(dates)
            ax.legend()

            # Attach a text label above each bar in rects1 and rects2, displaying its height.
            for rects in [rects1, rects2]:
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            fig.tight_layout()

        st.pyplot(plt)

        # Additional weather updates
        forecaster = mgr.forecast_at_place(place, '3h')
        
        # Check for impending weather changes
        st.write("## Impending Temperature Changes :")
        if forecaster.will_have_rain():
            st.write("Rain expected!")
        elif forecaster.will_have_clear():
            st.write("Clear Weather!")
        if forecaster.will_have_fog():
            st.write("Fog expected!")
        if forecaster.will_have_clouds():
            st.write("Cloudy weather expected!")
        if forecaster.will_have_snow():
            st.write("Snow expected!")
        if forecaster.will_have_storm():
            st.write("Storm expected!")
        if forecaster.will_have_tornado():
            st.write("Tornado expected!")
        if forecaster.will_have_hurricane():
            st.write("Hurricane expected!")

        # Current weather details
        observation = mgr.weather_at_place(place)
        weather = observation.weather

        # Cloud coverage and wind speed
        cloud_coverage = weather.clouds
        wind_speed = weather.wind()['speed']

        st.write("## Cloud coverage and wind speed")
        st.write(f"The current cloud coverage for {place} is {cloud_coverage}%")
        st.write(f"The current wind speed for {place} is {wind_speed} mph")

        # Sunrise and Sunset Times
        sunrise_time = datetime.datetime.utcfromtimestamp(weather.sunrise_time()).strftime('%Y-%m-%d %H:%M:%S')
        sunset_time = datetime.datetime.utcfromtimestamp(weather.sunset_time()).strftime('%Y-%m-%d %H:%M:%S')

        st.write("## Sunrise and Sunset Times :")
        st.write(f"Sunrise time in {place} is {sunrise_time} IST")
        st.write(f"Sunset time in {place} is {sunset_time} IST")

    except Exception as e:
        st.write(f"Error: {e}")