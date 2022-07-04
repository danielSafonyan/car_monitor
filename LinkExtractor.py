from bs4 import BeautifulSoup
import requests
import sys
import time
import csv
import socket



class CarLinkExtractor:
    __all_links = []
    __car_dicts = []
    __url = f"https://www.autoscout24.com/lst/ford/mustang/bt_coupe?" \
            f"fregfrom=2015&fregto=2018&kmto=50000&body=3&sort=price&desc=0&bcol=14%2C11&&page=1"

    __num_offers = None
    __num_pages = None

    @classmethod
    def __get_link_list(cls):
        cls.__get_num_offers_pages(cls.__url)
        time.sleep(1)
        print("Driving mustangs to the stalls.\n")
        cls.__extract_links()
        print('\nA list of cars is ready.')
        print(cls.__all_links)
        return cls.__all_links

    @classmethod
    def __get_soup(cls, url):
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        r = requests.get(url, headers=headers)

        if r.ok:
            pass
        else:
            sys.exit(f"The request returned {r.status_code} status code.")

        return BeautifulSoup(r.content, 'html.parser')

    @classmethod
    def __get_num_offers_pages(cls, url):
        soup = cls.__get_soup(url)
        num_offers = soup.find('header', class_="ListHeader_header__0Alte").find('h1').get_text().lower().split()[0]
        cls.__num_offers = int(num_offers)

        if num_offers:
            num_pages = soup.find_all('li', class_='pagination-item')[-1].get_text()
            cls.__num_pages = int(num_pages)
            message = f'Found {num_offers} offers for Ford Mustang on {num_pages} pages.'
            print(message)
        else:
            sys.exit(f"Didn't find any offers for Ford Mustang.")

    @classmethod
    def __extract_links(cls):
        for page_num in range(1, cls.__num_pages + 1):
            print(f'Going through the {page_num} page.')
            url = cls.__url.replace('page=1', f'page={page_num}')
            soup = cls.__get_soup(url)
            page_results = soup.find_all('div', class_='ListItem_wrapper__J_a_C')
            for result in page_results:
                link = 'https://www.autoscout24.com' \
                       + result.find('div', class_='ListItem_header__uPzec').find('a')['href']
                cls.__all_links.append(link)

    @classmethod
    def __get_year(cls, vehicle_overview, link):
        try:
            year = vehicle_overview[2].get_text().split('/')[1]
        except Exception:
            print("Couldn't get a year!")
            print(link)
            return 0
        try:
            return int(year)
        except ValueError:
            print(f'Year should be a natural number, not {year}.')
            print(link)
            return 0

    @classmethod
    def __get_mileage(cls, vehicle_overview, link):
        try:
            mileage = vehicle_overview[0].get_text()
        except Exception:
            print("Couldn't get the mileage.")
            print(link)
            return 0
        chars = [' km', ',']
        for ch in chars:
            mileage = mileage.replace(ch, '')
        try:
            return float(mileage)
        except ValueError:
            print(f'Mileage should be a real number, not {mileage}.')
            return 0

    @classmethod
    def __get_price(cls, soup, link):
        price = soup.find('span', class_='css-1b5kt8d').get_text()
        chars = ['€', ',', '-']
        for ch in chars:
            try:
                price = price.replace(ch, '')
            except Exception:
                print(f'Price should be a real number, not {price}.')
                print(link)
                return 0
        try:
            return float(price)
        except ValueError:
            print(f'Price should be a real number, not {price}.')
            print(link)
            return 0

    @classmethod
    def __get_location(cls, soup, link):
        try:
            location = soup.find('a', class_='scr-link css-4uy6qb').get_text()
        except Exception:
            print('Location is not specified!')
            print(link)
            location = 'Unknown'
        return location

    @classmethod
    def __get_specification(cls, soup, link):
        try:
            specification = soup.find('div', class_='css-l08njs').get_text()
        except Exception:
            print('Car has no spec!')
            print(link)
            specification = 'None'
        return specification

    @classmethod
    def __extract_car_info(cls):
        cls.__get_link_list()
        for link in cls.__all_links:
            print('Scraping an offer.')
            soup = cls.__get_soup(link)
            specification = cls.__get_specification(soup, link)
            location = cls.__get_location(soup, link)
            price = cls.__get_price(soup, link)
            vehicle_overview = soup.find_all('div', class_='VehicleOverview_itemText__V1yKT')
            mileage = cls.__get_mileage(vehicle_overview, link)
            year = cls.__get_year(vehicle_overview, link)
            try:
                img_url = soup.find('picture').find('img')['src']
            except Exception:
                print('Car has no img url!')
                img_url = 'None'
                print(link)

            this_car = {
                'link': link,
                'specification': specification,
                'location': location,
                'price': price,
                'mileage': mileage,
                'year': year,
                'img_url': img_url,
            }

            cls.__car_dicts.append(this_car)
        print('\nFinished extracting links.')

    @classmethod
    def save_to_csv(cls):
        cls.__extract_car_info()
        with open('mustangs.csv', 'w') as file:
            fieldnames = ['link', 'specification', 'location', 'price', 'mileage', 'year', 'img_url']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for car in CarLinkExtractor.__car_dicts:
                writer.writerow(car)
        print('Finished writing to csv.')


CarLinkExtractor.save_to_csv()
