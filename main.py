import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint


def _get_headers():
    headers = Headers(browser="firefox", os="win").generate()
    return headers

def vacancy_tag_all(HOST):
    hh_main_html = requests.get(HOST, headers=_get_headers()).text
    soup = BeautifulSoup(hh_main_html, features="lxml")
    vacancy_list_tag = soup.find(class_="vacancy-serp-content")
    vacancy_tags = vacancy_list_tag.find_all('a', class_='serp-item__title')
    return vacancy_tags

def _find_vacancy(link):
    vacancy_html = requests.get(link, headers=_get_headers()).text
    vacansy_body = BeautifulSoup(vacancy_html, features='lxml').find(
                   'div', class_='vacancy-description').text
    pattern = r"(.*django.*flask.*)|(.*flask.*django.*)"
    result = re.findall(pattern, vacansy_body, flags=re.I)
    return result

def vacancy_list(data):
    vacancy_list = []
    vacancy_list_json = []
    for vac in data:
        link = vac['href']
        x = _find_vacancy(link)
        if len(x) > 0:
            vacancy_list.append(vac)
            # vacancy_html = requests.get(HOST, headers=_get_headers()).text
            # city_name = BeautifulSoup(vacancy_html, features='lxml').find('div', class_="vacancy-serp-item__info")
            # city = city_name.find('div', class_="bloko-text").text
            # print(city)
    
    for vac in vacancy_list:    
        vacancy_link = vac['href']
        vacancy_html = requests.get(vacancy_link, headers=_get_headers()).text
        vacancy_tag = BeautifulSoup(vacancy_html, features='lxml')
        vacancy_name = vacancy_tag.find(
                        'h1', class_='bloko-header-section-1').text
        vacancy_salary = vacancy_tag.find(
                        'span', class_='bloko-header-section-2 bloko-header-section-2_lite').text
        company = vacancy_tag.find(
                 'div', class_='vacancy-company-details').text
        
        vacancy_city = BeautifulSoup(vac, features='lxml')
        pprint(vacancy_city)
        # city = BeautifulSoup(vac, features='lxml') # vacancy_tag.find('a', class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited")
        # city_name = city.find()
        # # city = _find_city(city_name)
        # print(vacancy_name)
        # print(vacancy_salary)
        # print(company)
        # pprint(city_name)
    return vacancy_list_json        

# def write_json(data):
    
      
if __name__ == '__main__':
    HOST = 'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&text=python'
    x = vacancy_tag_all(HOST)
    y = vacancy_list(x)
    # pprint(x)
# pprint(len(vacancy_tags)
 