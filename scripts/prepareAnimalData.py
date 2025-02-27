import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Datei-Pfad
file_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData\observations.csv"

# Deployment-IDs und zugehörige Kamera-Namen
deployment_mapping = {
    "088807f7-414f-4028-a24e-9e5d32c7a413": "Camera 1",  # von Max
    "aa8b4d44-1da6-4783-820a-25e88db504db": "Camera 2",  # Elias
    "70a31176-9505-4a50-9af5-4a7905f4cb60": "Camera 3",  # neu
}

try:
    # CSV-Datei einlesen
    data = pd.read_csv(file_path)

    # Filtern nach gültigen Deployment-IDs
    filtered_data = data[data['deploymentID'].isin(deployment_mapping.keys())]

    # Zusätzlicher Filter: Nur Einträge mit observationType == "animal"
    filtered_data = filtered_data[filtered_data['observationType'] == "animal"]

    # Spalte 'deploymentID' in 'Camera' umbenennen
    filtered_data = filtered_data.rename(columns={'deploymentID': 'Camera'})

    # Deployment-IDs durch Kameranamen ersetzen
    filtered_data['Camera'] = filtered_data['Camera'].map(deployment_mapping)


    # Funktion zur Datumsanpassung für eventStart und eventEnd
    def adjust_timestamp(ts):
        try:
            dt = datetime.strptime(ts[:-6], "%Y-%m-%dT%H:%M:%S")  # Entfernt Zeitzone
            tz_offset = ts[-6:]  # Speichert Zeitzoneninfo (z.B. +01:00)

            if dt.year == 2019:
                dt += relativedelta(years=4, months=9, days=3) + timedelta(hours=19)

            return dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_offset  # Fügt Zeitzone wieder hinzu
        except (ValueError, TypeError):
            return ts  # Falls das Format nicht stimmt, bleibt das Originaldatum


    # Falls 'eventStart' und 'eventEnd' Spalten existieren, Datumsanpassung durchführen
    for col in ['eventStart', 'eventEnd']:
        if col in filtered_data.columns:
            filtered_data[col] = filtered_data[col].astype(str).apply(adjust_timestamp)

    # Löschen der Spalten 'observationID', 'mediaID', 'eventID'
    columns_to_drop = ['observationID', 'mediaID', 'eventID']
    filtered_data = filtered_data.drop(columns=columns_to_drop, errors='ignore')

    # Neuer Datei-Pfad
    output_file_path = os.path.join(
        os.path.dirname(file_path), "filtered_observations.csv"
    )

    # Gefilterte Daten speichern
    filtered_data.to_csv(output_file_path, index=False)

    print(f"Gefilterte Daten wurden gespeichert unter: {output_file_path}")

except FileNotFoundError:
    print("Die Datei wurde nicht gefunden. Bitte überprüfe den Datei-Pfad.")
except pd.errors.EmptyDataError:
    print("Die Datei scheint leer zu sein.")
except KeyError as e:
    print(f"Die benötigte Spalte wurde nicht gefunden: {e}")
