import pandas as pd
import os
import glob

# Ordner-Pfade
input_folder_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\rawData"
output_folder_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\Data"

# Muster für Dateien, die gemerged werden sollen
file_pattern = os.path.join(input_folder_path, "Wetter*.csv")

# Liste aller passenden Dateien
csv_files = glob.glob(file_pattern)

# Überprüfen, ob Dateien gefunden wurden
if not csv_files:
    print("Keine passenden Dateien gefunden.")
else:
    try:
        # Alle CSV-Dateien einlesen und zusammenführen
        merged_data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

        # Prüfung und Bearbeitung der Spalten
        # 1. 'snow': Leere Werte durch 0 ersetzen und in Integer konvertieren
        if 'snow' in merged_data.columns:
            merged_data['snow'] = merged_data['snow'].fillna(0).astype(int)
            print("Leere Werte in der Spalte 'snow' wurden mit 0 gefüllt.")
        else:
            print("Spalte 'snow' nicht gefunden. Es wurden keine Änderungen vorgenommen.")

        # 2. 'date': Sicherstellen, dass die Spalte existiert und korrekt formatiert ist
        if 'date' in merged_data.columns:
            merged_data['date'] = pd.to_datetime(merged_data['date'], format='%Y-%m-%d')

            # Spalte 'day_of_year' hinzufügen
            merged_data['day_of_year'] = merged_data['date'].dt.dayofyear

            # Fehlende Werte in anderen Spalten auffüllen und auf eine Nachkommastelle runden
            for col in merged_data.columns:
                if col not in ['date', 'day_of_year', 'snow']:
                    merged_data[col] = merged_data.groupby('day_of_year')[col].transform(
                        lambda group: group.fillna(round(group.mean(), 1) if not pd.isna(group.mean()) else 0)
                    )

            # Temporäre Spalte 'day_of_year' entfernen
            merged_data.drop(columns=['day_of_year'], inplace=True)
            print("Fehlende Werte in den anderen Spalten wurden aufgefüllt und gerundet.")
        else:
            print("Spalte 'date' nicht gefunden. Keine weiteren Bearbeitungen durchgeführt.")

        # Sicherstellen, dass der Ausgabeordner existiert
        os.makedirs(output_folder_path, exist_ok=True)

        # Datei speichern
        output_file_path = os.path.join(output_folder_path, "merged_weather_data.csv")
        merged_data.to_csv(output_file_path, index=False)

        print(f"Die Dateien wurden erfolgreich gemerged und bearbeitet. Gespeichert unter: {output_file_path}")
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Dateien: {e}")
