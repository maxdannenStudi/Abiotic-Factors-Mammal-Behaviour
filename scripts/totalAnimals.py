import pandas as pd
import matplotlib.pyplot as plt

# Load the provided CSV file
observations_file = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\filtered_observations.csv"
output_image_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs\Totalanimals_by_camera.png"

# Read the observation data
observations_data = pd.read_csv(observations_file)

# Group the data by scientificName and Camera and count occurrences
camera_animal_counts = observations_data.groupby(['scientificName', 'Camera']).size().unstack(fill_value=0)

# Calculate total counts per animal
total_counts = camera_animal_counts.sum(axis=1)

# Create a stacked bar chart
plt.figure(figsize=(12, 6))
ax = camera_animal_counts.plot(
    kind='bar', stacked=True, figsize=(12, 6), color=plt.cm.Paired.colors, edgecolor='black'
)

# Annotate bars with total count per animal
for i, animal in enumerate(camera_animal_counts.index):
    total = total_counts[animal]
    ax.text(i, total + 1, f"{total}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

# Customize the chart
plt.title('Frequency of Photographed Animals by Camera', fontsize=16)
plt.xlabel('Animal Name', fontsize=12)
plt.ylabel('Number of Photos', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(title='Camera', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the updated bar chart
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
print(f"Graph saved successfully at: {output_image_path}")

# Show the plot
plt.show()

# Create a dictionary to store the summary for each camera
camera_animal_summary = {}

# Iterate through each camera and record the animals it captured and their counts
for camera in camera_animal_counts.columns:
    captured_animals = camera_animal_counts[camera][camera_animal_counts[camera] > 0]
    total_count = captured_animals.sum()

    animal_details = "\n  ".join([f"{animal}: {count}" for animal, count in captured_animals.items()])

    camera_animal_summary[camera] = f"**{camera}** (Total: {total_count} captures):\n  {animal_details}"

# Combine all summaries into one text
full_animal_camera_summary = "\n\n".join(camera_animal_summary.values())

# Print the full summary
print(full_animal_camera_summary)
