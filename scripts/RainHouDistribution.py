import pandas as pd
import matplotlib.pyplot as plt

# File paths
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
weather_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\merged_weather_data.csv"
output_image_path_rain = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_rain.png"
output_image_path_no_rain = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_no_rain.png"

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

# Filter by rain conditions
rain_days = capreolus_data[capreolus_data["prcp"] > 0]
no_rain_days = capreolus_data[capreolus_data["prcp"] == 0]

# Define hours (0-23)
hours = range(24)

# Count sightings by hour, ensuring all hours are represented
rain_counts = rain_days["hour"].value_counts().reindex(hours, fill_value=0)
no_rain_counts = no_rain_days["hour"].value_counts().reindex(hours, fill_value=0)

# Barplot for rainy days
plt.figure(figsize=(10, 6))
rain_counts.plot(kind="bar", color="blue", edgecolor="black")
plt.title("Capreolus capreolus - Sightings per Hour (Rainy Days)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Sightings", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_rain, dpi=300)
plt.show()

# Barplot for no-rain days
plt.figure(figsize=(10, 6))
no_rain_counts.plot(kind="bar", color="orange", edgecolor="black")
plt.title("Capreolus capreolus - Sightings per Hour (No Rain Days)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Sightings", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_no_rain, dpi=300)
plt.show()

# Summary of rain conditions
days_with_rain = weather_data[weather_data["prcp"] > 0]["date"].nunique()
days_without_rain = weather_data[weather_data["prcp"] == 0]["date"].nunique()

print(f"Summary of Days (2022-2024):")
print(f"Days with Rain: {days_with_rain}")
print(f"Days without Rain: {days_without_rain}")

print(f"Graphs saved at:\n- {output_image_path_rain}\n- {output_image_path_no_rain}")
