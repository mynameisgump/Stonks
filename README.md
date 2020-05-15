![Stonks Man](https://i.kym-cdn.com/entries/icons/original/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg)
# Stonks
Stonks bot is a simple bot which generates financial market information graphs from info provided by the Alpha Vantage api. 
I am hoping to implement more features, such as the ability to adjust the time period as well as generate graphs based off
of other financial indicators. Stonks bot also has the ability to generate graphs for cryptocurrencies as well. I am also 
planning on potentially making the bot more modular to allow for alternate financial apis.

# Usage
```
Stonks$ {stock|crypto} [ARG]
```
The argument must be the ticker for the stock or crypto. I am hoping to also implement a feature to search for these tickers.
As an example:
```
Stonks$ crypto BTC
```
would generate:

![BTC Graph](https://media.discordapp.net/attachments/688110160010412058/689267758453489714/graph.png?width=586&height=421)

```
Stonks$ IBM intraday 1min
```
![IBM Graph](https://cdn.discordapp.com/attachments/688110160010412058/710838357634318406/graph.png)
