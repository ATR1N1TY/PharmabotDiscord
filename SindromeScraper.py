from bs4 import BeautifulSoup
import requests

Dname = str(input('ჩაწერეთ დაავადების სახელი ქართულად: '))
#1149 daavadeba aris agwerili bazashi

def Get_DeseaseURL():

    First_letter = Dname[0]

    Searching_Wletter = requests.get(f"http://gh.ge/ka/diseases/{First_letter}/")
    Search_page = BeautifulSoup(Searching_Wletter.text, 'html.parser')

    symptoms_box = Search_page.find('a', string = Dname)

    global D_link
    D_link = symptoms_box.get('href')

    scrape_info()

def scrape_info():
    Get_Dpage = requests.get(D_link)
    Disease_Page = BeautifulSoup(Get_Dpage.text, 'html.parser')
    Demo_text = Disease_Page.find('div',class_ = 'text').text
    print(Demo_text)

Get_DeseaseURL()

