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

- fastapi <br>
- uvicorn<br>

SQLite<br>
sqlite3 <br>
Download [here](https://www.sqlite.org/download.html)

Tulip Indicators <br>

- tulipy <br>

Alpaca <br>

- alpaca_trade_api <br>

UI <br>
[Tradingview widgets](https://github.com/tradingview/lightweight-charts) <br>
[Chart.js](https://www.chartjs.org/docs/latest/getting-started/) <br>
[Jinja2 Templates](https://fastapi.tiangolo.com/advanced/templates/) <br>

Other <br>

- requests <br>
- DateTime <br>
- pytrends <br>
- pygooglenews <br>
- pandas <br>
- numpy <br>

Javascript libaries:
jQuery

## Contents

**[Home](https://github.com/K-minutti/stockgraph#home)** <br>
**[Screener](https://github.com/K-minutti/stockgraph#screener)** <br>
**[Single View](https://github.com/K-minutti/stockgraph#single-view)** <br>
**[Order History](https://github.com/K-minutti/stockgraph#order-history)** <br>
**[Study](https://github.com/K-minutti/stockgraph#study)** <br>

### Home

The home is the base page and is the first thing you see when entering the site. The page was built using CSS grid and it displays data from the DB as well as data from google trends, and google news by using the packages pytrends and pygooglenews. The charts use Chart.js and TradingView Lightweight Charts.

### Screener

The screener is for end of day screening and doesn't display intraday data. The data is pulled from the DB. The percentage change as well as the indicators are computed using numpy and the tulip indicators library.

### Single View

To see information on individual stocks use the searchbar or click on the company names when using the screener. <br>

This view features a tradingview chart, company news, stocktwists feed and a side bar with the following information:<br>
company financials <br>
analyst ratings <br>
related companies <br>
strategy <br>

### Order History

Note: To see order history you need access to your Alpaca trading account.

### Study

IP: This section shows andvance analysis on one stock at a time.
