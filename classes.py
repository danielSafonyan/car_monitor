from datetime import date
from bs4 import BeautifulSoup
import requests
import sys


def get_num_offers(soup):
    num_offers = soup.find('header', class_="ListHeader_header__0Alte").find('h1').get_text().lower().split()[0]
    num_offers = int(num_offers)

    if num_offers:
        num_pages = soup.find_all('li', class_='pagination-item')[-1].get_text()
        num_pages = int(num_pages)
        header = f'Found {num_offers} offers for Ford Mustang on {num_pages} pages.'
        print(header)
        return num_offers, num_pages
    else:
        sys.exit(f"Didn't find any offers for Ford Mustang.")


def get_owners(owners, url):
    try:
        return int(owners)
    except ValueError:
        print("Number of previous owners unknown.")
        print(url)
        return None


def get_year(year):
    try:
        return int(year)
    except ValueError:
        print(f'Year should be a natural number, not {year}.')
        return None


def get_mileage(mileage: str):
    chars = [' km', ',']
    for ch in chars:
        mileage = mileage.replace(ch, '')
    try:
        return float(mileage)
    except ValueError:
        print(f'Mileage should be a real number, not {mileage}.')
        return None


def get_price(price: str):
    chars = ['€', ',', '-']
    for ch in chars:
        price = price.replace(ch, '')
    try:
        return float(price)
    except ValueError:
        print(f'Price should be a real number, not {price}.')
        return None


def get_soup(url):
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    r = requests.get(url, headers=headers)

    if r.ok:
        print("Page loaded successfully!")
    else:
        sys.exit(f"The request returned {r.status_code} status code.")

    return BeautifulSoup(r.content, 'html.parser')


class Mustang:
    all_mustangs = []
    current_year = date.today().year

    def __init__(self, title: str, url: str, year: int, price: str, mileage: str, owners: int):
        self.spec = title
        self.url = url
        self.year = get_year(year)
        self.price = get_price(price)
        self.miles = get_mileage(mileage)
        self.owners = get_owners(owners, url)

        print("Mustang Object Created")
        Mustang.all_mustangs.append(self)

    def __repr__(self):
        return f'Mustang({self.spec}, {self.year}, {self.miles}, {self.owners})'

    def __str__(self):
        return f'Ford Mustang "{self.spec}", {self.year}, {self.miles} miles, {self.owners} owners.'

    def calc_yearly_mileage(self):
        yearly_mileage = self.miles / (self.current_year - self.year)
        yearly_mileage = round(yearly_mileage, 2)
        print(f'This mustang ran {yearly_mileage} miles per year!')
        return yearly_mileage

    @classmethod
    def instances_from_url(cls):
        url = f'https://www.autoscout24.com/lst/ford/mustang/bt_coupe?' \
              f'fregfrom=2015&fregto=2018&kmto=50000&body=3&sort=price&desc=0&bcol=14%2C11&&page=1'
        soup = get_soup(url)
        num_offers, num_pages = get_num_offers(soup)

        print("Driving mustangs to the stalls.\n")

        for page_num in range(1, num_pages + 1):
            url = f'https://www.autoscout24.com/lst/ford/mustang/bt_coupe?' \
                  f'fregfrom=2015&fregto=2018&kmto=50000&body=3&sort=price&desc=0&bcol=14%2C11&' \
                  f'page={page_num}'
            print(url)
            soup = get_soup(url)
            page_results = soup.find_all('div', class_='ListItem_wrapper__J_a_C')

            for result in page_results:
                # img_src = result.find('img')['src']
                url = 'https://www.autoscout24.com' + result.find('div', class_='ListItem_header__uPzec').find('a')[
                    'href']
                title = "Ford Mustang " + result.find('span', class_='ListItem_version__jNjur').get_text()
                price = result.find('p', class_='Price_price__WZayw').get_text()
                attributes = result.find_all('span', class_='VehicleDetailTable_item__koEV4')
                Mustang(
                    title=title,
                    url=url,
                    price=price,
                    mileage=attributes[0].get_text(),
                    year=attributes[1].get_text().split('/')[1],
                    owners=attributes[4].get_text().split()[0]
                )


