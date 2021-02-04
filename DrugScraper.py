import requests
from bs4 import BeautifulSoup

def Drug_scraper():
    global GeneralInfo, DetailedInfo
    DrugName = str(input('ჩაწერეთ წამლის სახელი ქართულად: '))
    SearchPage = requests.get(f'http://www.vidal.ge/search?query={DrugName}')
    SearchPageContent = BeautifulSoup(SearchPage.text, 'html.parser')
    PageCaption = SearchPageContent.find('figcaption', class_ = 'col-xs-10').h6.a
    DrugLink = PageCaption.get('href')
    DrugPage = requests.get(DrugLink)
    DrugPageContent = BeautifulSoup(DrugPage.text, 'html.parser')
    GeneralInfo = DrugPageContent.find('div', class_ = 'col-xs-12 col-sm-7 p_x_0').get_text()
    DetailedInfo = DrugPageContent.find('figcaption', class_ = 'item-info').get_text()

Drug_scraper()