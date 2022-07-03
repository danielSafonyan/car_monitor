import csv

with open('mustangs.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for line in csv_reader:
        print(line)