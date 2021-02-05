import discord
from discord import client
from discord.errors import ClientException
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import requests
import textwrap

client = commands.Bot(command_prefix = '+')

@client.event
async def on_ready():
    print('bot ready')


@client.command(aliases = ['წამალი'])
async def DrugInfo(ctx, Drugname):

    #Firstly we search for drug on vidals search page and then we convert that to content
    SearchPage = requests.get(f'http://www.vidal.ge/search?query={Drugname}')
    SearchPageContent = BeautifulSoup(SearchPage.content, 'html.parser')

    #Then we search for Drug URL, go to that link and convert that into content
    PageCaption = SearchPageContent.find('figcaption', class_ = 'col-xs-10').h6.a
    DrugLink = PageCaption.get('href')
    DrugPage = requests.get(DrugLink)
    DrugPageContent = BeautifulSoup(DrugPage.content, 'html.parser')

    #Then we scrape text from that page
    GeneralInfo = DrugPageContent.find('div', class_ = 'col-xs-12 col-sm-7 p_x_0').get_text()
    DetailedInfo = DrugPageContent.find('figcaption', class_ = 'item-info').get_text()
    
    await ctx.send(textwrap.wrap(DetailedInfo, 2000))



client.run('ODA2OTUxNjYwOTgyNjMyNDQ5.YBw6TA._mk7TbfMKc6vjzV4vCuMVcL9ahs')