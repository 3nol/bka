import requests
from bs4 import BeautifulSoup
import json


def indent_units(text: str, units: int = 1) -> str:
    return units * ' ' + text.replace('\n', '\n' + units * ' ')


class BKA:
    """Enables access to a wanted list of persons in JSON format"""

    def __init__(self):
        self.site = 'https://www.bka.de'
        self.list = '/SiteGlobals/Forms/Suche/Fahndungsliste_Personenfahndung_Formular.html?nn=4210&gtp=3922_list%253D'

    def get_wanted_persons(self, depth: int):
        """Retrieves json wanted list, parameter depth determines how often more entries should be loaded"""

        for i in range(depth):
            soup = BeautifulSoup(requests.get(self.site + self.list + str(i + 1)).text, 'html.parser')
            for person in soup.find_all('div', class_='slide teaser type-2'):
                img = self.site + person.find('img').get('src').split(';', 1)[0] + '?__blob=normal'
                category = str(person.find('span', class_='category').text).strip()
                name = str(person.find('h3').text).strip().replace('\u00ad', '')
                info = ''
                for fact in str(person.find('p').text).strip().split('\n'):
                    if fact != '':
                        (key, value) = fact.split(':', 1)
                        info += f'"{key}": "{value}",\n'

                json_string = '{\n' + indent_units(
                    f'"category": "{category}",\n'
                    f'"img": "{img}",\n'
                    f'"name": "{name}",\n'
                    '"info": {\n'
                    f'{indent_units(info, 2)}\n'
                    '}', 2) + '\n},'

                print(indent_units(json_string, 2))
                return json.loads(json_string)

