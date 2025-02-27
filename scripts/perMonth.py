import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# File paths
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
output_image_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Capreolus_monthly_observations_with_seasons.png"

# Read observations file
observations_data = pd.read_csv(observations_file)

# Extract month from the eventStart column
observations_data["eventStart"] = pd.to_datetime(observations_data["eventStart"], errors="coerce")
observations_data["month"] = observations_data["eventStart"].dt.month

# Filter for Capreolus capreolus
capreolus_data = observations_data[observations_data["scientificName"] == "Capreolus capreolus"]

# Count observations per month
monthly_counts = capreolus_data["month"].value_counts().sort_index()

# Define breeding and fawning periods
breeding_season = [7, 8]  # July-August
fawning_period = [5, 6]   # May-June

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the bar chart for monthly observations
bars = ax.bar(monthly_counts.index, monthly_counts.values, color="skyblue", edgecolor="black")

# Add labels to the bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, int(height), ha="center", va="bottom", fontsize=10)

# Add custom legend for the indicators
legend_handles = [

]
ax.legend(handles=legend_handles, loc="upper right", fontsize=10)

# Customize the chart
ax.set_title("Monthly Observations of Capreolus capreolus", fontsize=16)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Number of Observations", fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
ax.set_ylim(bottom=-3)  # Extend the y-axis to show the indicator below the chart

# Save the chart
plt.tight_layout()
plt.savefig(output_image_path, dpi=300, bbox_inches="tight")
print(f"Graph saved successfully at: {output_image_path}")

# Show the chart
plt.show()
