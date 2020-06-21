FROM python:3

ADD bot.py /

RUN pip install mplfinance

RUN pip install discord

RUN pip install alpha_vantage

RUN pip install python-dotenv

RUN pip install pprint

CMD [ "python", "./bot.py" ]
