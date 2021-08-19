import requests
from bs4 import BeautifulSoup


url = 'https://www.bka.de/SiteGlobals/Forms/Suche/Fahndungsliste_Personenfahndung_Formular.html?nn=4210&gtp=3922_list%253D'


def get_wanted_persons(depth: int) -> None:
    for i in range(depth):
        soup = BeautifulSoup(requests.get(url + str(i + 1)).text, 'html.parser')
        for person in soup.find_all('div', class_='textContainer'):
            print(person.text)

