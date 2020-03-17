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
        data, meta_data = cc.get_digital_currency_daily(symbol=args[2], market='USD')
        data.rename(index= pd.to_datetime,columns = {"1b. open (USD)":"Open","2b. high (USD)":"High","3b. low (USD)":"Low","4b. close (USD)":"Close","5. volume":"Volume"},inplace = True)
        data = data.iloc[::-1]
        mpf.plot(data,type="line",savefig="graph.png",title="Price chart for "+args[2])
        print("Finished crypto plot creation")
        await message.channel.send(file=discord.File('graph.png'))

    if args[1] == "stock":
        CUR = "CAD"
        ts = TimeSeries(key=ALPHA_TOKEN, output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=args[2],interval='1min', outputsize='full')
        data.rename(index= pd.to_datetime,columns = {"1. open":"Open","2. high":"High","3. low":"Low","4. close":"Close","5. volume":"Volume"},inplace = True)
        data = data.replace("",np.nan)
        data.index=pd.to_datetime(data.index)
        data = data.iloc[::-1]
        data.resample("1 min")
        plt.title("Testing")
        mpf.plot(data,type="line",savefig="graph.png")
        print("Finished stock plot creation")
        await message.channel.send(file=discord.File('graph.png'))

client.run(DISCORD_TOKEN)
