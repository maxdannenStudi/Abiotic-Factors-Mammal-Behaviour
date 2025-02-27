import pandas as pd
import os

# File paths
observations_file = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\rawData\\filtered_observations.csv"
output_folder = r"C:\\Users\\maxda\\Uni\\SUS3\\WeatherAnimalData2025\\Data"
output_file = os.path.join(output_folder, "sightings.csv")

# Generate date range: 01.01.2022 to 31.12.2024
date_range = pd.date_range(start="2022-01-01", end="2024-12-31", freq="D")
sightings_df = pd.DataFrame({"date": date_range})
sightings_df["date"] = sightings_df["date"].dt.strftime("%Y-%m-%d")  # Format YYYY-MM-DD

try:
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Load observations data
    observations_data = pd.read_csv(observations_file)

    # Convert eventStart to datetime and extract date in YYYY-MM-DD format
    observations_data["eventStart"] = pd.to_datetime(observations_data["eventStart"], errors="coerce")
    observations_data["eventDate"] = observations_data["eventStart"].dt.strftime("%Y-%m-%d")

    # Ensure the "count" column is numeric
    observations_data["count"] = pd.to_numeric(observations_data["count"], errors="coerce").fillna(0)

    # Get all distinct scientificNames
    distinct_scientific_names = observations_data["scientificName"].dropna().unique()

    # Add a column for each distinct scientificName, initialized with 0
    for name in distinct_scientific_names:
        sightings_df[name] = 0

    # Group data by eventDate and scientificName, summing the counts
    grouped_data = observations_data.groupby(["eventDate", "scientificName"]).agg({
        "count": "sum"
    }).reset_index()

    # Add the counts to the sightings_df
    for index, row in grouped_data.iterrows():
        event_date = row["eventDate"]
        scientific_name = row["scientificName"]
        total_count = row["count"]

        # Check if the event_date exists in sightings_df
        if event_date in sightings_df["date"].values:
            sightings_df.loc[sightings_df["date"] == event_date, scientific_name] += total_count

    # Berechne die Summe aller Spalten außer "date"
    sightings_df["totalCount"] = sightings_df.loc[:, sightings_df.columns != "date"].sum(axis=1)

    # Optionale Prüfung: Gesamtspalte hinzufügen und in einer separaten Datei speichern

    # Save the results as a CSV file
    sightings_df.to_csv(output_file, index=False)
    print(f"Sightings table successfully created and saved at: {output_file}")

except FileNotFoundError:
    print(f"The file {observations_file} was not found.")
except Exception as e:
    print(f"Error: {e}")
