import bs4.element
import requests
from bs4 import BeautifulSoup
import json


def indent_units(text: str, units: int = 1):
    """Enables pretty printing for the json string by indenting entries"""
    return units * ' ' + text.replace('\n', '\n' + units * ' ')


class BKA:
    """Enables access to a wanted list of persons in JSON format"""

    def __init__(self):
        # main website
        self.site = 'https://www.bka.de'
        # appendix for the wanted list
        self.list = '/SiteGlobals/Forms/Suche/Fahndungsliste_Personenfahndung_Formular.html?nn=4210&gtp=3922_list%253D'

    def get_wanted_persons(self, depth: int):
        """Retrieves json wanted list, parameter depth determines how often more entries should be loaded"""
        wanted_persons_list = ''
        for i in range(depth):
            soup = BeautifulSoup(requests.get(self.site + self.list + str(i + 1)).text, 'html.parser')
            persons = soup.find_all('div', class_='slide teaser type-2')
            for p in range(len(persons)):
                wanted_persons_list += '{\n' + indent_units(
                    f'"category": "{self.__get_category(persons[p])}",\n'
                    f'"img": "{self.__get_img(persons[p])}",\n'
                    f'"name": "{self.__get_name(persons[p])}",\n'
                    '"info": {\n'
                    f'{indent_units(self.__get_info(persons[p]), 2)}\n'
                    '}', 2) + '\n}'
                if i < depth - 1 or p < len(persons) - 1:
                    wanted_persons_list += ','
        wanted_persons_list = '[\n' + indent_units(wanted_persons_list, 2) + '\n]'
        print(wanted_persons_list)
        return json.loads(wanted_persons_list)

    def __get_img(self, person: bs4.element.Tag):
        """Retrieves the image url"""
        img_container = person.find('img')
        if img_container is not None:
            return self.site + img_container.get('src').split(';', 1)[0] + '?__blob=normal'
        return ''

    def __get_category(self, person: bs4.element.Tag):
        """Retrieves the entry category, e.g. 'Gesucht'"""
        category_container = person.find('span', class_='category')
        if category_container is not None:
            return str(category_container.text).strip()
        return ''

    def __get_name(self, person: bs4.element.Tag):
        """Retrieves the person's name (sometimes unknown)"""
        name_container = person.find('h3')
        if name_container is not None:
            return str(name_container.text).strip().replace('\u00ad', '')
        return ''

    def __get_info(self, person: bs4.element.Tag):
        """Collects all further information listed on the site, e.g. 'Delikt', 'Tatort', ..."""
        info_container = person.find('p')
        if info_container is not None:
            info = ''
            for fact in str(info_container.text).strip().split('\n'):
                if fact != '':
                    (key, value) = fact.split(':', 1)
                    info += f'"{key}": "{value}",\n'
            return info.rsplit(',\n', 1)[0]
        return ''
