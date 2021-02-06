import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import json


client = commands.Bot(command_prefix = '+')

@client.event
async def on_ready():
    print('bot ready')

#ინფორმაცია ბოტის შესახებ
@client.command(aliases = ['გამარჯობა','დახმარება'])
async def Hello(ctx):

    info = [
        'გამარჯობა, მე ვარ ფარმაბოტი შენ შეგიძლია შემეკითხო: ',
        '1.ინფორმაცია წამალზე: |+წამალი წამლის_სახელი|',
        '2.ინფორმაცია დაავადებაზე: |+დაავადება დაავადების_სახელი|',
        '3.ინფორმაცია COVID-19-ზე: |"+კორონა მსოფლიოში ან ქვეყნის სახელი ინგლისურად|"',
        '4.ინფორმაცია პირველად დახმარებაზე: |+პირველადი დახმარება|'
        ]

    for line in info:
        await ctx.send(line)

#წამლის სქრეიფერი
@client.command(aliases = ['წამალი'])
async def DrugInfo(ctx, *, Drugname):

    await ctx.send('მოიცა მოვძებნო...')

    try:

        # Search for the drug on vidal's search page and get a BS4 Object from the source
        SearchPage = requests.get(f'http://www.vidal.ge/search?query={Drugname}')
        SearchPageContent = BeautifulSoup(SearchPage.content, 'html.parser')

        # Search for the drug's URL and get a BS4 object from it
        Page_caption = SearchPageContent.find('figcaption', class_ = 'col-xs-10').h6.a
        Drug_link = Page_caption.get('href')
        Drug_page = requests.get(Drug_link)
        soup = BeautifulSoup(Drug_page.content, 'html.parser')

        # Scrape text from the page
        general_info = soup.find('div', class_ = 'col-xs-12 col-sm-7 p_x_0').get_text('\n', strip = True)

        # Send to discord
        await ctx.send(f'წამლის სახელწოდება: {Drugname}\nიხილეთ სრულად: {Drug_link} \n {general_info}')

    except Exception:

        await ctx.send('ვერ ვიპოვე, ეცადე ქართულად და სრულად მითხრა წამლის სახელი')

#დაავადების სქრეიფერი
@client.command(aliases = ['დაავადება'])
async def DiseaseInfo(ctx, *, Disease_name):

    await ctx.send('მოიცა მოვძებნო...')

    try:
        # Get & search disease by first letter of the disease's name
        First_letter = Disease_name[0]
        Searching_letter = requests.get(f"http://gh.ge/ka/diseases/{First_letter}/")
        Search_page = BeautifulSoup(Searching_letter.text, 'html.parser')

        # find disease page URL
        symptoms_box = Search_page.find('a', string = Disease_name)
        D_link = symptoms_box.get('href')

        # Scrape text from disease page
        Get_Dpage = requests.get(D_link)
        soup = BeautifulSoup(Get_Dpage.text, 'html.parser')
        Demo_text = soup.find('div',class_ = 'text').text

        # Send to discord
        await ctx.send(f'დაავადების სახელი: {Disease_name}\nიხილეთ სრულად: {D_link}\n{Demo_text}')

    except Exception:
        # Send to discord
        await ctx.send('ეგეთი დაავადება ვერ ვიპოვე, ეცადე სრულად და ქართულად მითხრა დაავადების სახელი')

#კორონას ქეისების სქრეიფერი
@client.command(aliases = ['კორონა'])
async def Global_COV(ctx, *, Country):

    # Get info about COVID from API
    Get_covid_info = requests.get('https://api.covid19api.com/summary')
    Covid_JSON = json.loads(Get_covid_info.text)

    # Translating case types
    Eng_to_geo = {'TotalConfirmed':'სულ:', 'TotalDeaths':'სიკვდილიანობა:', 'NewConfirmed':'ახალი დადასტურებული:', 'NewDeaths':'ახალი გარდაცვლილები:'}

    # Selecting & sending data from JSON to discord
    if Country == 'მსოფლიოში':
         for case in Eng_to_geo:
             await ctx.send(f"{Eng_to_geo[case]} {Covid_JSON['Global'][case]}")
    else:
        for case in Covid_JSON["Countries"]:
            if case['Country'] == Country:
                for x in Eng_to_geo:
                    await ctx.send(f"{Eng_to_geo[x]} {case[x]}")
                  
#ინფორმაცია პირველად დახმარებაზე
@client.command(aliases = ['პირველადი_დახმარება'])
async def First_aid(ctx):

    # Send to discord
    await ctx.send('პირველად დახმარებაზე ინფორმაციას ნახავ აქ: http://higia.ge/ka/healthDetailed/161/484/481/')


client.run('')