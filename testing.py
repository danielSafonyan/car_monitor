from bs4 import BeautifulSoup

with open('list_item2.html') as html:
    soup = BeautifulSoup(html, 'html.parser')
    re = soup.find('img')['src']
    print(re)