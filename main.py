from bs4 import BeautifulSoup
import requests
import sys

url = f'https://www.autoscout24.com/lst/ford/mustang/bt_coupe?' \
      f'fregfrom=2015&fregto=2018&kmto=50000&body=3&sort=price&desc=0&bcol=14%2C11&&page=1'
headers = {'Accept-Language': 'en-US,en;q=0.5'}


def get_soup():
    r = requests.get(url, headers=headers)

    if r.ok:
        print("URL loaded successfully!")
    else:
        sys.exit(f"The request returned {r.status_code} status code.")

    return BeautifulSoup(r.content, 'html.parser')

soup = get_soup()
# the number of pages returned by search query
# used [-1] to get the value of the last <li> element
num_offers = soup.find('header', class_="ListHeader_header__0Alte").find('h1').get_text().lower().split()[0]
num_offers = int(num_offers)

if num_offers:
    num_pages = soup.find_all('li', class_='pagination-item')[-1].get_text()
    num_pages = int(num_pages)
    header = f'Found {num_offers} offers for Ford Mustang on {num_pages} pages.'
    print(header)
else:
    sys.exit(f"Didn't find any offers for Ford Mustang.")

print("Driving mustangs to the stalls.")
mustang_list = []

for page_num in range(1, num_pages + 1):
    url = f'https://www.autoscout24.com/lst/ford/mustang/bt_coupe?' \
          f'fregfrom=2015&fregto=2018&kmto=50000&body=3&sort=price&desc=0&bcol=14%2C11&' \
          f'page={page_num}'
    print(url)
    soup = get_soup()
    page_results = soup.find_all('div', class_='ListItem_wrapper__J_a_C')

    for result in page_results:
        # img_src = result.find('img')['src']
        link = 'https://www.autoscout24.com' + result.find('div', class_='ListItem_header__uPzec').find('a')['href']
        title = "Ford Mustang " + result.find('span', class_='ListItem_version__jNjur').get_text()
        price = result.find('p', class_='Price_price__WZayw').get_text()
        attributes = result.find_all('span', class_='VehicleDetailTable_item__koEV4')
        this_car = {
            'title': title,
            'link': link,
            # 'img_src': img_src,
            'price': price,
            'mileage': attributes[0].get_text(),
            'year': attributes[1].get_text().split('/')[1],
            'previous owners': attributes[4].get_text().split()[0]
        }
        mustang_list.append(this_car)

print(mustang_list)