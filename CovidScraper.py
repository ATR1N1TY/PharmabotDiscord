from sys import int_info
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz

qveyana = str(input('ჩაწერეთ ქვეყნის სახელი ინგლისურად: '))

#კოვიდი ქვეყნებისთვის
def Covid(country):
    Case_list = ['სულ:','სიკვდილიანობა:', 'გამოჯანმრთელებული:']

    if country == "":
        Covid_page = requests.get(f'https://www.worldometers.info/coronavirus/')
        soup = BeautifulSoup(Covid_page.text, 'html.parser')
        Covid_numbers = soup.find_all('div', class_ = 'maincounter-number')

    else:        
        Covid_page = requests.get(f'https://www.worldometers.info/coronavirus/country/{country}')
        soup = BeautifulSoup(Covid_page.text, 'html.parser')
        Covid_numbers = soup.find_all('div', class_ = 'maincounter-number')

        
        GMT_time = datetime.now(tz=tz.gettz("Europe/London")).strftime("%Y-%m-%d")
        Updates_part = soup.find(id=f'newsdate{GMT_time}')
        text = Updates_part.find_all('strong')

        new_cases = text[0].get_text()
        new_deaths = text[1].get_text()
        
    for n in range(3):
        Total_Cases = Covid_numbers[n].get_text(strip = True)
        print(Case_list[n], Total_Cases)

    caseNUM = []
    DeathNUM = []

    for char in new_cases:                
        if char != 'n':
            caseNUM.append(char)
        else:
            print('დღეს დაინფიცირებული:', ''.join(caseNUM))

    for char in new_deaths:
        if char !='n':
            DeathNUM.append(char)
        else:
            print('დღეს გარდავლილი:', ''.join(DeathNUM))
                
    
    


Covid(qveyana)

def Covid_test(country):
    d = 1
