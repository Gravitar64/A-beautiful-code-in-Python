from Google_Maps_Credentials import APIKey
import googlemaps
import csv

zeilen = []
with open('Teil_07_origins_destinations.csv') as f:
  readCSV = csv.reader(f)
  for zeile in readCSV:
    zeilen.append(zeile)

destinations = zeilen[0]
origins = zeilen[1]

gmaps = googlemaps.Client(key=APIKey)
distances = gmaps.distance_matrix(origins, destinations)

zeile = ['']+distances['destination_addresses']
output = [zeile]

for n, row in enumerate(distances['rows']):
  zeile = []
  zeile.append(distances['origin_addresses'][n])
  for ziel in row['elements']:
    zeile.append(ziel['duration']['value'])
  output.append(zeile)

with open('Entfernungsmatrix3.csv', 'w', newline='') as f:
  writer = csv.writer(f)
  writer.writerows(output)
