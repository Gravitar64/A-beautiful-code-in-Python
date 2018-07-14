from Google_Maps_Credentials import API_Key
import googlemaps
import csv

csvZeilen = []
with open('origins_destinations.csv') as f:
    readCSV = csv.reader(f)
    for zeile in readCSV:
        csvZeilen.append(zeile)

origins = csvZeilen[0]
destinations = csvZeilen[1]

gmaps = googlemaps.Client(key=API_Key)
distances = gmaps.distance_matrix(destinations, origins)

output = [['']+distances['destination_addresses']]

for n, zeile in enumerate(distances['rows']):
    row = []
    row.append(distances['origin_addresses'][n])
    for ziel in zeile['elements']:
        row.append(ziel['duration']['value'])
    output.append(row)

with open('Entfernungsmatrix2.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(output)
