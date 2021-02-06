import requests
from bs4 import BeautifulSoup

DrugName = 'ვენოდიოლი' #str(input('ჩაწერეთ წამლის სახელი ქართულად: '))
print('გთხოვთ მოიცადოთ, მიმდინარეობს წამლის ძიება...')

def Drug_Scraper(Name):

    #Firstly we search for drug on vidals search page and then we convert that to content
    SearchPage = requests.get(f'http://www.vidal.ge/search?query={Name}')
    SearchPageContent = BeautifulSoup(SearchPage.content, 'html.parser')

    #Then we search for Drug URL, go to that link and convert that into content
    PageCaption = SearchPageContent.find('figcaption', class_ = 'col-xs-10').h6.a
    DrugLink = PageCaption.get('href')
    DrugPage = requests.get(DrugLink)
    DrugPageContent = BeautifulSoup(DrugPage.content, 'html.parser')

    #Then we scrape text from that page
    GeneralInfo = DrugPageContent.find('div', class_ = 'col-xs-12 col-sm-7 p_x_0').get_text('|', strip = True)
    DetailedInfo = DrugPageContent.find('figcaption', class_ = 'item-info').get_text()
    print(GeneralInfo)

Drug_Scraper(DrugName)
