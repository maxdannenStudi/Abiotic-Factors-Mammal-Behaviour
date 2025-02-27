import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path
input_file = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\Data\\merged_output.csv"
output_image = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\graphs\\correlation_matrix.png"

try:
    # Load the merged dataset
    merged_data = pd.read_csv(input_file)

    # Define the two groups of columns
    animal_columns = ["Lepus europaeus", "Capreolus capreolus", "Canis lupus familiaris",
                      "Vulpes vulpes", "Capra hircus", "Turdus", "totalCount"]
    weather_columns = ["tavg", "tmin", "tmax", "prcp", "pres",]

    # Ensure the columns exist in the dataset
    filtered_data = merged_data[animal_columns + weather_columns]

    # Handle constant or NaN values
    filtered_data = filtered_data.dropna()  # Drop rows with NaN values
    filtered_data = filtered_data.loc[:, filtered_data.std() > 0]  # Drop constant columns

    # Calculate correlations strictly between the two groups
    correlation_values = {
        animal: [
            filtered_data[animal].corr(filtered_data[weather])
            for weather in weather_columns
        ]
        for animal in animal_columns
    }

    # Convert to a DataFrame for heatmap
    correlation_df = pd.DataFrame(correlation_values, index=weather_columns).T

    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_df, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.xlabel("Weather Metrics")
    plt.ylabel("Animal Metrics")
    plt.title("Correlation Matrix Heatmap (Animals vs Weather Data)")

    # Save the heatmap as an image file
    plt.savefig(output_image)
    print(f"Correlation matrix heatmap successfully created and saved at: {output_image}")

except FileNotFoundError as e:
    print(f"File not found: {e}")
except KeyError as e:
    print(f"Missing column in the dataset: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
