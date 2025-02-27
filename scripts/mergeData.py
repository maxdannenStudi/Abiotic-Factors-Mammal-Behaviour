import pandas as pd

# File paths
weather_data_file = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\Data\\merged_weather_data.csv"
sightings_data_file = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\Data\\sightings.csv"
output_file = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\Data\\merged_output.csv"

try:
    # Load weather and sightings data
    weather_data = pd.read_csv(weather_data_file)
    sightings_data = pd.read_csv(sightings_data_file)

    # Ensure date columns are in the same format
    weather_data["date"] = pd.to_datetime(weather_data["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    sightings_data["date"] = pd.to_datetime(sightings_data["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Merge the two datasets on the "date" column
    merged_data = pd.merge(weather_data, sightings_data, on="date", how="inner")

    # Save the merged dataset to a CSV file
    merged_data.to_csv(output_file, index=False)
    print(f"Merged data successfully created and saved at: {output_file}")

except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
