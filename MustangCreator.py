from LinkExtractor import CarLinkExtractor

class Mustang:
    all_mustangs = []

    def __init__(self, specification, location, price, mileage, year, img_url):
        self.__specification = specification
        self.__location = location
        self.__price = price
        self.__mileage = mileage
        self.__year = year
        self.__img_url = img_url

        print('Mustang created.')
        Mustang.all_mustangs.append(self)

    def __str__(self):
        return f'This is a Ford Mustang {self.__specification}'

    @classmethod
    def create_mustang_objects(cls, car_dicts):
        for dict_ in car_dicts:
            Mustang(
                specification=dict_['specification'],
                location=dict_['location'],
                price=dict_['price'],
                mileage=dict_['mileage'],
                year=dict_['year'],
                img_url=dict_['img_url'],
            )