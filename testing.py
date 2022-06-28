from bs4 import BeautifulSoup

with open('list_item2.html') as html:
    soup = BeautifulSoup(html, 'html.parser')
    re = soup.find('div', class_='ListItem_header__uPzec').find('a')['href']
    print(re)