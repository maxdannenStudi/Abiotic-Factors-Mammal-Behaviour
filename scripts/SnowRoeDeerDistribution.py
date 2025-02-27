import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File paths
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
weather_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\merged_weather_data.csv"

# Read files
observations_data = pd.read_csv(observations_file)
weather_data = pd.read_csv(weather_file)

# Extract date from observations
observations_data["eventStart"] = pd.to_datetime(observations_data["eventStart"], errors="coerce")
observations_data["eventDate"] = observations_data["eventStart"].dt.strftime("%Y-%m-%d")

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

# Define snow depth bins (e.g., no snow, light, moderate, heavy)
snow_bins = [0, 1, 5, 10, 20, 50]  # Adjust as needed
snow_labels = [f"{snow_bins[i]} to {snow_bins[i+1]} cm" for i in range(len(snow_bins)-1)]

# Add a snow depth bin column
capreolus_data["snow_bin"] = pd.cut(capreolus_data["snow"], bins=snow_bins, labels=snow_labels, right=False)
weather_data["snow_bin"] = pd.cut(weather_data["snow"], bins=snow_bins, labels=snow_labels, right=False)

# Count actual captures per snow bin
actual_counts = capreolus_data["snow_bin"].value_counts().sort_index()

# Count days per snow bin
days_per_bin = weather_data["snow_bin"].value_counts().sort_index()

# Total days and total deer captures
total_days = days_per_bin.sum()
total_deer_captures = actual_counts.sum()

# Calculate expected captures per snow bin
expected_counts = (days_per_bin / total_days) * total_deer_captures

# Create a summary DataFrame
summary = pd.DataFrame({
    "Snow Depth Range": snow_labels,
    "Actual Captures": actual_counts.values,
    "Expected Captures": expected_counts.values,
    "Days": days_per_bin.values
}).fillna(0)

# Add a percentage difference column
summary["Percentage Difference"] = (
    (summary["Actual Captures"] - summary["Expected Captures"]) / summary["Expected Captures"]
) * 100

# Print the summary
print(summary)

# Bar plot for actual vs expected captures
plt.figure(figsize=(12, 8))
x = np.arange(len(snow_labels))  # X positions for bars
width = 0.4  # Bar width

# Plot actual and expected captures
plt.bar(x - width/2, summary["Actual Captures"], width=width, color="skyblue", edgecolor="black", label="Actual Captures")
plt.bar(x + width/2, summary["Expected Captures"], width=width, color="orange", edgecolor="black", label="Expected Captures")

# Add numbers on top of the bars
for i in range(len(summary)):
    plt.text(x[i] - width/2, summary["Actual Captures"].iloc[i] + 1,
             int(summary["Actual Captures"].iloc[i]), ha="center", fontsize=10)
    plt.text(x[i] + width/2, summary["Expected Captures"].iloc[i] + 1,
             f"{summary['Expected Captures'].iloc[i]:.1f}", ha="center", fontsize=10)

# Customize plot
plt.title("Actual vs Expected Capreolus capreolus Sightings by Snow Depth", fontsize=16)
plt.xlabel("Snow Depth Range (cm)", fontsize=12)
plt.ylabel("Number of Captures", fontsize=12)
plt.xticks(x, snow_labels, rotation=45, ha="right")
plt.legend(loc="upper right")
plt.tight_layout()

# Show plot
plt.show()
