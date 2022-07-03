import csv
import copy


class Mustang:
    __all_mustangs = []

    @classmethod
    def get_mustang_list(cls):
        return copy.deepcopy(cls.__all_mustangs)

    def __init__(self, link, specification, location, price, mileage, year, img_url):
        self.link = link
        self.__specification = specification
        self.__location = location
        self.__price = price
        self.__mileage = mileage
        self.__year = year
        self.__img_url = img_url

        print('Mustang created.')
        Mustang.__all_mustangs.append(self)

    def __str__(self):
        return f'This is a Ford Mustang {self.__specification}'

    def __repr__(self):
        return f'Ford Mustang {self.__specification}'

    @classmethod
    def create_mustang_objects_from_csv(cls):
        with open('mustangs.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for line in csv_reader:
                Mustang(
                    link=line['link'],
                    specification=line['specification'],
                    location=line['location'],
                    price=line['price'],
                    mileage=line['mileage'],
                    year=line['year'],
                    img_url=line['img_url'],
                )


Mustang.create_mustang_objects_from_csv()
print(Mustang.get_mustang_list())
