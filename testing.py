import csv


class CarLinkExtractor:
    car_dicts = []

    @classmethod
    def save_to_csv(cls):
        pass

this_car = {
    'specification': "GT",
    'location': "USA",
    'price': "21",
}

for i in range(5):
    CarLinkExtractor.car_dicts.append(this_car)

for i in CarLinkExtractor.car_dicts:
    print(i)

with open('mustangs.csv', 'w') as file:
    fieldnames = ['specification', 'location', 'price']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for car in CarLinkExtractor.car_dicts:
        writer.writerow(car)


