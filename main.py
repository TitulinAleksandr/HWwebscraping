import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint


HOST = "https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&text=python"

def get_headers():
    headers = Headers(browser="firefox", os="win").generate()
    return headers

def find_vacancy(link):
    vacancy_html = requests.get(link, headers=get_headers()).text
    vacansy_body = BeautifulSoup(vacancy_html, features='lxml').find('div', class_='vacancy-description')
    pattern = r"(.*django.*flask.*)|(.*flask.*django.*)"
    result = re.findall(pattern, vacansy_body, flags=re.I)
    if pattern in result:
        return result
    else:
        pass   
hh_main_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_main_html, features="lxml")
vacancy_list_tag = soup.find(class_="vacancy-serp-content")
vacancy_tags = vacancy_list_tag.find_all('a', class_='serp-item__title')
vacancy = []

for vac in vacancy_tags:
    link = vac['href']
    vacancy_html = requests.get(link, headers=get_headers()).text
    vacansy_body = BeautifulSoup(vacancy_html, features='lxml').find('div', class_='vacancy-description')
    pprint(vacansy_body)   

# pprint(len(vacancy_tags)
       