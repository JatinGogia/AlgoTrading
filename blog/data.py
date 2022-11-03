from cmath import rect
import requests
import json
from newsapi import NewsApiClient
import pycountry



def fetchCompanyData(cmpName):
    f = open('StockCode.json')
    data=json.load(f)
    url = (f'''https://newsapi.org/v2/everything?q={data[cmpName]}&from=2022-11-01&sortBy=popularity&apiKey=07b2c6a4274c43a399ad60bf453b81fe''')
    response = requests.get(url)
    if len(response.json()['articles'])==0:
        return f"No News available for {cmpName}"

    return response.json()['articles']


def RecentNews():
    newsapi = NewsApiClient(api_key='07b2c6a4274c43a399ad60bf453b81fe')
    input_country ="India"
    input_countries = [f'{input_country.strip()}']
    countries = {}

    for country in pycountry.countries:
        countries[country.name] = country.alpha_2

    codes = [countries.get(country.title(), 'Unknown code')
            for country in input_countries]

    top_headlines = newsapi.get_top_headlines(category=f'{"Business".lower()}', language='en', country=f'{codes[0].lower()}')
    Headlines = top_headlines['articles']
    news=[]
    if Headlines:
            for articles in Headlines:
                b = articles['title'][::-1].index("-")
                if "news" in (articles['title'][-b+1:]).lower():
                    news.append(f"{articles['title'][-b+1:]}: {articles['title'][:-b-2]}.")
                else:
                    news.append(f"{articles['title'][-b+1:]} News: {articles['title'][:-b-2]}.")
    return news 

