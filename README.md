# Stockgraph

### About

Stockgraph is a web app to explore the stock market and individual stocks.

![repo-home](https://user-images.githubusercontent.com/58534537/116260472-b74fb100-a744-11eb-9ec6-ab247585c8e6.png)

---

## Notes

This app uses the FastAPI framework you can learn more about it [here](https://fastapi.tiangolo.com/).

A full list of the libaries and pacakages used can be found below. One important to note is that the price data
used comes from [Alpaca](https://alpaca.markets/docs/). Alpaca is a an API provider for algorithimic traders. You will need to sign up for an account in order to receive an API key.

Once you have your credentials create a config.py file to store your API_KEY and SECRET_KEY.

Data for this app is updated at the end of the day. It uses crontab jobs to run the populate_prices.py file in the db folder. Cron should be installed in most MacOS and Linux distributions. Click [here](https://www.hostinger.com/tutorials/cron-job) for a quick walk through on cron.

### Requirements

FastAPI<br>
fastapi==0.63.0 <br>
uvicorn==0.13.4 <br>

SQLite<br>
sqlite3 <br>
Download [here](https://www.sqlite.org/download.html)

Tulip Indicators <br>
tulipy==0.3.1 <br>

Alpaca <br>
alpaca_trade_api <br>

UI <br>
tradingview widgets <br>
chart.js <br>
Jinja2 Template <br>

Other <br>
requests <br>
DateTime <br>
pytrends <br>
pygooglenews <br>
pandas <br>
numpy <br>

## Contents

[**Home**]
**Screener**
**Single View**
**Order History**
**Study**

### Home

-APIs that is uses

### Screener

-Function

### Single View
