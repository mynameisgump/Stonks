# bot.py
import os
import discord
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

import mplfinance as mpf
    
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.techindicators import TechIndicators
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ALPHA_TOKEN = os.getenv('ALPHA_TOKEN')
PREFIX = "Stonks$"

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return
    args = message.content.split(" ");
    print(args);

    if args[0] != PREFIX:
        return

    if args[1] == "ping":
        await message.channel.send("pong!")

    #Stonks$ {crypto/stock} {ticker} {date}
    if args[1] == "crypto":
        CUR = "CAD"
        cc = CryptoCurrencies(key=ALPHA_TOKEN, output_format='pandas')
        data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='CNY')
        data['4b. close (USD)'].plot()
        plt.tight_layout()
        plt.title('Daily close value for bitcoin (BTC)')
        plt.grid()
        plt.show()
        plt.savefig('foo.png')
        print("Finished plot creation")

    if args[1] == "stock":
        CUR = "CAD"
        ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='full')
        data = data.reset_index(drop=True)
        print(data.head(2))
        pd.Dataframe(index= pd.to_datetime,columns = lambda x : x.split(' ')[-1],inplace = True)
        print(data.head(2))
        data["4. close"].plot()
        #data['4. close'].plot()
        plt.title('Intraday Times Series for the MSFT stock (1 min)')
        plt.show()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print("Test")
CUR = "CAD"
ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AMD',interval='1min', outputsize='full')
print(data.head(2))
#data.rename(index= pd.to_datetime,columns = lambda x : x.split(' ')[-1],inplace = True)
data.rename(index= pd.to_datetime,columns = {"1. open":"Open","2. high":"High","3. low":"Low","4. close":"Close","5. volume":"Volume"},inplace = True)
data = data.replace("",np.nan)
data.index=pd.to_datetime(data.index)
data.iloc[::-1]
data.resample("1 min")
print(data.head(60))
mpf.plot(data,type ="line")
data["4. close"].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()
client.run(DISCORD_TOKEN)
