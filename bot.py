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
        ts = TimeSeries(key=ALPHA_TOKEN, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=args[2],interval='1min', outputsize='full')
        data.rename(index= pd.to_datetime,columns = {"1. open":"Open","2. high":"High","3. low":"Low","4. close":"Close","5. volume":"Volume"},inplace = True)
        data = data.replace("",np.nan)
        data.index=pd.to_datetime(data.index)
        data = data.iloc[::-1]
        data.resample("1 min")
        mpf.plot(data,type ="line")
client.run(DISCORD_TOKEN)
