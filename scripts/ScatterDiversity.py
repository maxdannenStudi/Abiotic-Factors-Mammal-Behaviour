import pandas as pd
import matplotlib.pyplot as plt
import os

# Datei-Pfad definieren
file_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\Data\merged_output.csv"
save_path = r"C:\Users\maxda\Uni\SUS3\WeatherAnimalData2025\graphs"

# Sicherstellen, dass das Speicherverzeichnis existiert
os.makedirs(save_path, exist_ok=True)

# CSV-Datei einlesen
df = pd.read_csv(file_path)

# Sicherstellen, dass Temperatur und Niederschlag numerisch sind
df['tavg'] = pd.to_numeric(df['tavg'], errors='coerce')
df['prcp'] = pd.to_numeric(df['prcp'], errors='coerce')

# Wetterspalten (Nicht-Tierarten)
weather_columns = ['date', 'tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']

# Alle anderen Spalten als Tierarten betrachten
species_columns = [col for col in df.columns if col not in weather_columns]

# Diversität berechnen: Anzahl der vorkommenden Tierarten pro Tag (Wert > 0)
df['Diversity'] = df[species_columns].gt(0).sum(axis=1)

# Nur Tage mit Diversität > 0 und gültiger Temperatur/Niederschlag berücksichtigen
df_filtered = df[(df['Diversity'] > 0) & df['tavg'].notna() & df['prcp'].notna()]

# Scatterplot erstellen: Regen vs. Temperatur, mit Farbe basierend auf Diversität
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df_filtered['prcp'], df_filtered['tavg'], c=df_filtered['Diversity'], cmap='viridis', alpha=0.8, edgecolors='black', linewidth=0.5)

# Colorbar hinzufügen
cbar = plt.colorbar(scatter)
cbar.set_label('Diversität (Anzahl unterschiedlicher Tierarten)', fontsize=12, fontweight='bold')

# Titel und Achsenbeschriftungen
plt.xlabel('Niederschlag (mm)', fontsize=12, fontweight='bold')
plt.ylabel('Durchschnittstemperatur (°C)', fontsize=12, fontweight='bold')
plt.title('Niederschlag, Temperatur & Diversität', fontsize=14, fontweight='bold')

# Gitter hinzufügen
plt.grid(color='gray', linestyle='--', linewidth=0.5)

# Hintergrundfarbe setzen für bessere Lesbarkeit
plt.gca().set_facecolor('#f0f0f0')

# Grafik speichern
graph_file = os.path.join(save_path, "rain_temperature_diversity.png")
plt.savefig(graph_file, dpi=300)

print(f"Die Grafik wurde gespeichert unter: {graph_file}")
