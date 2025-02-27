import pandas as pd
import matplotlib.pyplot as plt

# File paths
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
weather_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\merged_weather_data.csv"
output_image_path_above = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_above_20.png"
output_image_path_below = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_below_20.png"
output_image_path_negative = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_negative_temp.png"

# Read files
observations_data = pd.read_csv(observations_file)
weather_data = pd.read_csv(weather_file)

# Extract date and hour from observations
observations_data["eventStart"] = pd.to_datetime(observations_data["eventStart"], errors="coerce")
observations_data["eventDate"] = observations_data["eventStart"].dt.strftime("%Y-%m-%d")
observations_data["hour"] = observations_data["eventStart"].dt.hour

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

# Filter for Capreolus capreolus
capreolus_data = merged_data[merged_data["scientificName"] == "Capreolus capreolus"]

# Filter by temperature ranges
above_20 = capreolus_data[capreolus_data["tavg"] > 20]
below_20 = capreolus_data[capreolus_data["tavg"] <= 20]
negative_temp = capreolus_data[capreolus_data["tavg"] < 0]

# Define hours (0-23)
hours = range(24)

# Count photos by hour, ensuring all hours are represented
above_20_counts = above_20["hour"].value_counts().reindex(hours, fill_value=0)
below_20_counts = below_20["hour"].value_counts().reindex(hours, fill_value=0)
negative_temp_counts = negative_temp["hour"].value_counts().reindex(hours, fill_value=0)

# Barplot for tavg > 20
plt.figure(figsize=(10, 6))
above_20_counts.plot(kind="bar", color="orange", edgecolor="black")
plt.title("Capreolus capreolus - Photos per Hour (tavg > 20°C)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Photos", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_above, dpi=300)

# Barplot for tavg <= 20
plt.figure(figsize=(10, 6))
below_20_counts.plot(kind="bar", color="blue", edgecolor="black")
plt.title("Capreolus capreolus - Photos per Hour (tavg <= 20°C)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Photos", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_below, dpi=300)

# Barplot for tavg < 0
plt.figure(figsize=(10, 6))
negative_temp_counts.plot(kind="bar", color="purple", edgecolor="black")
plt.title("Capreolus capreolus - Photos per Hour (tavg < 0°C)", fontsize=16)
plt.xlabel("Hour of the Day", fontsize=12)
plt.ylabel("Number of Photos", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_image_path_negative, dpi=300)

# Summary of temperature conditions
days_above_20 = weather_data[weather_data["tavg"] > 20]["date"].nunique()
days_below_20 = weather_data[weather_data["tavg"] <= 20]["date"].nunique()
days_negative_temp = weather_data[weather_data["tavg"] < 0]["date"].nunique()

print(f"Summary of Days (2022-2024):")
print(f"Days with tavg > 20°C: {days_above_20}")
print(f"Days with tavg <= 20°C: {days_below_20}")
print(f"Days with tavg < 0°C: {days_negative_temp}")
