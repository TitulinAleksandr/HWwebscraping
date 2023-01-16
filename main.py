import requests
import re
import json
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
                
    for vac in vacancy_list:    
        vacancy_link = vac['href']
        vacancy_html = requests.get(vacancy_link, headers=_get_headers()).text
        vacancy_tag = BeautifulSoup(vacancy_html, features='lxml')
        vacancy_title = vacancy_tag.find(
                        'h1', class_='bloko-header-section-1').text
        vacancy_salary = vacancy_tag.find(
                        'span', class_='bloko-header-section-2 bloko-header-section-2_lite').text
        company = vacancy_tag.find(
                 'div', class_='vacancy-company-details').text
        city_name = vacancy_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        vacancy_list_json.append({'title':vacancy_title, 'link': vacancy_link,
                                  'company': company, 'city':city_name, 'salary': vacancy_salary})  
        
    return vacancy_list_json        

def write_json(data):
    with open ('job_list.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


     
if __name__ == '__main__':
    HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    x = vacancy_tag_all(HOST)
    y = vacancy_list(x)
    write_json(y)
