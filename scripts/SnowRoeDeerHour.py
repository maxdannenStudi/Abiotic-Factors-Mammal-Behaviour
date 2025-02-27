import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File paths
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
weather_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\merged_weather_data.csv"
output_image_path_snow = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_snow.png"
output_image_path_no_snow = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_no_snow.png"

# Read files
observations_data = pd.read_csv(observations_file)
weather_data = pd.read_csv(weather_file)

# Convert 'eventStart' to datetime and extract date and hour
observations_data["eventStart"] = pd.to_datetime(observations_data["eventStart"], errors="coerce")
observations_data["eventDate"] = observations_data["eventStart"].dt.strftime("%Y-%m-%d")
observations_data["hour"] = observations_data["eventStart"].dt.hour  # Extract hour of sightings

# Format date in weather data
weather_data["date"] = pd.to_datetime(weather_data["date"]).dt.strftime("%Y-%m-%d")

# Merge observations with weather data on date
merged_data = pd.merge(
    observations_data,
    weather_data,
    left_on="eventDate",
    right_on="date",
    how="inner"
)

# Filter for Capreolus capreolus sightings
capreolus_data = merged_data[merged_data["scientificName"] == "Capreolus capreolus"]

# Filter by snow conditions
snow_days = capreolus_data[capreolus_data["snow"] > 0]
no_snow_days = capreolus_data[capreolus_data["snow"] == 0]

# Define hours (0-23)
hours = range(24)

# Count sightings by hour, ensuring all hours are represented
snow_counts = snow_days["hour"].value_counts().reindex(hours, fill_value=0)
no_snow_counts = no_snow_days["hour"].value_counts().reindex(hours, fill_value=0)

# Barplot for snowy days
plt.figure(figsize=(10, 6))
snow_counts.plot(kind="bar", color="blue", edgecolor="black")
plt.title("Capreolus capreolus - Sightings per Hour (Snowy Days)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Sightings", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_snow, dpi=300)
plt.show()

# Barplot for no-snow days
plt.figure(figsize=(10, 6))
no_snow_counts.plot(kind="bar", color="orange", edgecolor="black")
plt.title("Capreolus capreolus - Sightings per Hour (No Snow Days)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Sightings", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_no_snow, dpi=300)
plt.show()

# Summary of snow conditions
days_with_snow = weather_data[weather_data["snow"] > 0]["date"].nunique()
days_without_snow = weather_data[weather_data["snow"] == 0]["date"].nunique()

print(f"Summary of Days (2022-2024):")
print(f"Days with Snow: {days_with_snow}")
print(f"Days without Snow: {days_without_snow}")

print(f"Graphs saved at:\n- {output_image_path_snow}\n- {output_image_path_no_snow}")
