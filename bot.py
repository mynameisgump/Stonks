# bot.py
import os
import discord
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import mplfinance as mpf
import numpy as np
import time as time
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
cc = CryptoCurrencies(key=ALPHA_TOKEN, output_format='pandas')
ts = TimeSeries(key=ALPHA_TOKEN, output_format='pandas')

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
        #cc = CryptoCurrencies(key=ALPHA_TOKEN, output_format='pandas')
        data, meta_data = cc.get_digital_currency_daily(symbol=args[2], market='USD')
        data.rename(index= pd.to_datetime,columns = {"1b. open (USD)":"Open","2b. high (USD)":"High","3b. low (USD)":"Low","4b. close (USD)":"Close","5. volume":"Volume"},inplace = True)
        data = data.iloc[::-1]
        mpf.plot(data,type="line",savefig="graph.png",title="Price chart for "+args[2])
        print("Finished crypto plot creation")
        await message.channel.send(file=discord.File('graph.png'))

    if args[1] == "stock":
        CUR = "CAD"
        #ts = TimeSeries(key=ALPHA_TOKEN, output_format='pandas')
        
        if args[3] == "intraday":
            try:
                interval = '1min'
                if len(args) > 4:
                    interval = args[4]
                data, meta_data = ts.get_intraday(symbol=args[2],interval=interval, outputsize='full')
                data.rename(index= pd.to_datetime,columns = {"1. open":"Open","2. high":"High","3. low":"Low","4. close":"Close","5. volume":"Volume"},inplace = True)
                data = data.replace("",np.nan)
                data.index=pd.to_datetime(data.index)
                data = data.iloc[::-1]
            except ValueError as err:
                await message.channel.send("Invalid Ticker")

        if args[3] == "daily":
            try:
                data, meta_data = ts.get_daily_adjusted(symbol=args[2],outputsize='full')
                data.rename(index= pd.to_datetime,columns = {"1. open":"Open","2. high":"High","3. low":"Low","4. close":"Close","5. adjusted close":"Adj Close","6. volume":"Volume"},inplace = True)
                data = data.replace("",np.nan)
                data.index=pd.to_datetime(data.index)
                data = data.iloc[::-1]
            except ValueError as err:
                await message.channel.send("Invalid Ticker")
        
        data = data[data.index > dt.datetime.now() - pd.to_timedelta("8day")]

        mpf.plot(data,savefig="graph.png",title="Price chart for "+args[2], style="yahoo")
        print("Finished stock plot creation")

        await message.channel.send(file=discord.File('graph.png'))

client.run(DISCORD_TOKEN)
