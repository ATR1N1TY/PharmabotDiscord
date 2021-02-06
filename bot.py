from typing import ContextManager
import discord
from discord import client
from discord.errors import ClientException
from discord.ext import commands
from bs4 import BeautifulSoup
import requests


client = commands.Bot(command_prefix = '+')

@client.event
async def on_ready():
    print('bot ready')

#წამლის სქრეიფერი
@client.command(aliases = ['წამალი'])
async def DrugInfo(ctx, *, Drugname):

    await ctx.send('მოიცა მოვძებნო...')
    try:

        #Firstly we search for drug on vidals search page and then we convert that to content
        SearchPage = requests.get(f'http://www.vidal.ge/search?query={Drugname}')
        SearchPageContent = BeautifulSoup(SearchPage.content, 'html.parser')

        #Then we search for Drug URL, go to that link and convert that into content
        PageCaption = SearchPageContent.find('figcaption', class_ = 'col-xs-10').h6.a
        DrugLink = PageCaption.get('href')
        DrugPage = requests.get(DrugLink)
        DrugPageContent = BeautifulSoup(DrugPage.content, 'html.parser')

        #Then we scrape text from that page
        DetailedInfo = DrugPageContent.find('figcaption', class_ = 'item-info').get_text()
    
        Demo_Dinfo = DetailedInfo[0:1500]

        await ctx.send(f'წამლის სახელწოდება: {Drugname}\nიხილეთ სრულად: {DrugLink} \n {Demo_Dinfo}')

    except Exception:

        await ctx.send('ვერ ვიპოვე, ეცადე ქართულად და სრულად მითხრა წამლის სახელი')

#დაავადების სქრეიფერი
@client.command(aliases = ['დაავადება'])
async def DiseaseInfo(ctx, *, Disease_name):

    await ctx.send('მოიცა მოვძებნო...')
    try:
        First_letter = Disease_name[0]

        Searching_Wletter = requests.get(f"http://gh.ge/ka/diseases/{First_letter}/")
        Search_page = BeautifulSoup(Searching_Wletter.text, 'html.parser')

        symptoms_box = Search_page.find('a', string = Disease_name)
        D_link = symptoms_box.get('href')

        Get_Dpage = requests.get(D_link)
        Disease_Page = BeautifulSoup(Get_Dpage.text, 'html.parser')
        Demo_text = Disease_Page.find('div',class_ = 'text').text
        
        await ctx.send(f'დაავადების სახელი: {Disease_name}\nიხილეთ სრულად: {D_link}\n{Demo_text}')
    except Exception:
        await ctx.send('ეგეთი დაავადება ვერ ვიპოვე, ეცადე სრულად და ქართულად მითხრა დაავადების სახელი')

#გლობალური კორონას ქეისების სქრეიფერი
@client.command(aliases = ['კორონა'])
async def Global_COV(ctx, *, Country):

    Case_list = ['სულ:','სიკვდილიანობა:', 'გამოჯანმრთელებული:']

    if Country == 'მსოფლიოში':
        Covid_Page = requests.get('https://www.worldometers.info/coronavirus/')
        soup = BeautifulSoup(Covid_Page.text, 'html.parser')
        Covid_numbers = soup.find_all('div', class_ = 'maincounter-number')

        for n in range(3):
            Total_Cases = Covid_numbers[n].get_text(strip = True)
            await ctx.send(f'{Case_list[n]} {Total_Cases}')
    else:
        

client.run('ODA2OTUxNjYwOTgyNjMyNDQ5.YBw6TA._mk7TbfMKc6vjzV4vCuMVcL9ahs')