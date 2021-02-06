from typing import Counter
import requests
import json

Get_covid_info = requests.get('https://api.covid19api.com/summary')
Covid_JSON = json.loads(Get_covid_info.text)

Eng_to_geo = {'TotalConfirmed':'სულ:', 'TotalDeaths':'სიკვდილიანობა:', 'NewConfirmed':'ახალი დადასტურებული:', 'NewDeaths':'ახალი გარდაცვლილები:'}

def Global_COVID():
    
    for x in Eng_to_geo:
        print(Eng_to_geo[x], Covid_JSON['Global'][x])

COUNTRY = str(input('enter name of country: '))

def Local_COVID(): 

    for C in Covid_JSON["Countries"]:
        if C['Country'] == COUNTRY:
            for x in Eng_to_geo:
                print(Eng_to_geo[x], C[x])

Local_COVID()


