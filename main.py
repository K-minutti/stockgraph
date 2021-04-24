from fastapi import FastAPI, Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import datetime
import time
import requests
import sqlite3
# import alpaca_trade_api as tradeapi
from pygooglenews import GoogleNews
gn = GoogleNews()
from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=300)


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
    

@app.get("/")
def index(request: Request):
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(""" 
        SELECT symbol, name, exchange FROM stock ORDER BY symbol
    """)
    all_stocks = cursor.fetchall()

    #Google trends 
    g_trends_df = pytrends.trending_searches(pn='united_states')
    google_trends_arr = g_trends_df.to_dict('records')
    google_trends = []
    count = 0
    for obj in google_trends_arr:
        count += 1
        google_trends.append({"count": count, "item": f"{obj[0]}"})
        
    #News API / Google News wrapper library
    # #props - title, link, published, published_parsed
    business = gn.topic_headlines('business')
    technology = gn.topic_headlines('technology')
    bus = business['entries']
    tech = technology['entries']
    bus_and_tech = bus + tech
    all_news = []
    for item in bus_and_tech:
        time_stamp = time.mktime(item['published_parsed'])
        date_as_dt = datetime.datetime.fromtimestamp(time_stamp) - datetime.timedelta(hours=4)
        date_str = date_as_dt.strftime('%m-%d')
        time_str = date_as_dt.strftime('%H:%M:%S')
        item['time_stamp'] = time_stamp
        item['date'] = date_str
        item['time'] = time_str
        all_news.append(item)
    def sort_by_key(obj):
        return obj['time_stamp']
    all_news.sort(key=sort_by_key, reverse=True)

    #we need the top stocks in a list of two tuples like below for the top stocks
    # cursor.execute(""" 
    #     SELECT symbol, change FROM historical_prices ORDER BY change DESC
    # """)
    # top_stocks = cursor.fetchall()
    #we need to make an object with the 5 symbols for the market overview {"SPY": [{"time": time, value: close}]}
    #each symbol needs a list of objects with time series data


    top_stocks = [
    ({"symbol": "WBT", "change": "44.47"}, {"symbol": "UFAB", "change": "-20.00"}),
    ({"symbol": "SKLZ", "change": "33.55"}, {"symbol": "DGLY", "change": "-11.86"}), 
    ({"symbol": "TYHT", "change": "31.50"}, {"symbol": "EBET", "change": "-10.18"}), 
    ({"symbol": "ASXC", "change": "30.26"}, {"symbol": "LVTX", "change": "-9.63"}), 
    ({"symbol": "GBOX", "change": "27.39"}, {"symbol": "BTX", "change": "-9.09"}), 
    ({"symbol": "TIPT", "change": "30.26"}, {"symbol": "JCOM", "change": "-8.51"}), 
    ({"symbol": "PLBY", "change": "26.27"}, {"symbol": "DSGN", "change": "-8.43"}), 
    ({"symbol": "BIVI", "change": "36.21"}, {"symbol": "PLAG", "change": "-8.33"})
    
    ]
    
    return templates.TemplateResponse("index.html", {"request": request,"top_stocks": top_stocks,  "news": all_news, "g_trends":google_trends, "ad_data": [2411, 320, 4046], "all_stocks": all_stocks})

@app.get("/stock/{symbol}")
def single_stock(request: Request, symbol):
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(""" 
        SELECT symbol, name, exchange FROM stock ORDER BY symbol
    """)
    all_stocks = cursor.fetchall()
    # cursor.execute(""" 
    #     SELECT * FROM strategy
    # """)
    # strategies = cursor.fetchall()
    # cursor.execute(""" 
    #     SELECT id, symbol, name FROM stock WHERE symbol = ?
    # """, (symbol,))
    # row = cursor.fetchone()
    # cursor.execute(""" 
    #     SELECT * FROM historical_prices WHERE stock_id = ? ORDER BY date DESC
    # """, (row['id'],))
    # prices = cursor.fetchall()

    #Ratings for sidebar
    #webscrapping module


    search = gn.search(f'NASDAQ:{symbol}', when = '6m') #for symbol stock.exchange:symbol
    # search_twp gn.search(f'{row.name}', when = '6m') #for name of company - this takes priority as results are better
    news_search = search['entries']
    news = []
    for item in news_search:
        time_stamp = time.mktime(item['published_parsed'])
        date_as_dt = datetime.datetime.fromtimestamp(time_stamp) - datetime.timedelta(hours=4)
        date_str = date_as_dt.strftime('%m-%d')
        time_str = date_as_dt.strftime('%H:%M:%S')
        item['time_stamp'] = time_stamp
        item['date'] = date_str
        item['time'] = time_str
        news.append(item)
    def sort_by_key(obj):
        return obj['time_stamp']
    news.sort(key=sort_by_key, reverse=True)

    s_twits = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")
    twits = s_twits.json()
    stock_twits = twits['messages']
    # for twit in stock_twits:

    stock = {"symbol": symbol, "name": symbol}
    return templates.TemplateResponse("single_stock.html", {"request": request, "stock": stock, "news":news, "stock_twits": stock_twits, "all_stocks": all_stocks})

@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    cursor.execute(""" 
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?)
    """, (stock_id, strategy_id))

    connection.commit()
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/screener")
def screener(request: Request):
    stock_filter = request.query_params.get('filter', False)
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
        cursor.execute(""" 
            select * from (
                select symbol, name, stock_id, max(close), date
                from historical_prices join stock on stock.id = historical_prices.stock_id
                group by stock_id
                order by symbol
            ) where date = (select max(date) from historical_prices)
        """)
    elif stock_filter == 'new_closing_lows':
        cursor.execute(""" 
            select * from (
                select symbol, name, stock_id, min(close), date
                from historical_prices join stock on stock.id = historical_prices.stock_id
                group by stock_id
                order by symbol
            ) where date = (select max(date) from historical_prices)
        """)
    elif stock_filter == 'rsi_overbought':
        cursor.execute(""" 
            select symbol, name, stock_id, date
            from historical_prices join stock on stock.id = historical_prices.stock_id
            where rsi_14 > 70
            AND date = (select max(date) from historical_prices)
            order by rsi_14 desc
        """)
    elif stock_filter == 'rsi_oversold':
        cursor.execute(""" 
            select symbol, name, stock_id, date
            from historical_prices join stock on stock.id = historical_prices.stock_id
            where rsi_14 < 30
            AND date = (select max(date) from historical_prices)
            order by rsi_14 asc
        """)
    elif stock_filter == 'under_sma_50':
        cursor.execute(""" 
            select symbol, name, stock_id, date
            from historical_prices join stock on stock.id = historical_prices.stock_id
            where close < sma_50
            AND date = (select max(date) from historical_prices)
            order by symbol
        """)
    elif stock_filter == 'over_sma_50':
        cursor.execute(""" 
            select symbol, name, stock_id, date
            from historical_prices join stock on stock.id = historical_prices.stock_id
            where close > sma_50
            AND date = (select max(date) from historical_prices)
            order by symbol
        """)
    else:
        cursor.execute(""" 
            select id, symbol, name from stock order by symbol
        """)
    rows = cursor.fetchall()

    cursor.execute(""" 
        select symbol, name, sma_20, sma_50, rsi_14, close
        from stock join historical_prices on historical_prices.stock_id = stock.id
        where date = (select max(date) from historical_prices)
    """)

    indicator_rows = cursor.fetchall()
    indicator_values = {}
    for row in indicator_rows:
        indicator_values[row['symbol']] = row

    cursor.execute(""" 
        select * from strategy
    """)

    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(""" 
        SELECT symbol, name, exchange FROM stock ORDER BY symbol
    """)
    all_stocks = cursor.fetchall()

    strategies = cursor.fetchall()
    return templates.TemplateResponse("screener.html", {"request" : request, "stocks": rows,  "indicator_values":indicator_values,"strategies": strategies, "all_stocks": all_stocks})

# @app.get("/orders")
# def orders(request: Request):
#     api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)
#     orders = api.list_orders(status="all")
#     return templates.TemplateResponse("orders.html", {"request" :request, "orders": orders})


@app.get("/study")
def study(request: Request):
    return templates.TemplateResponse("study.html", {"request":request})

@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(""" 
        SELECT id, name 
        FROM strategy
        WHERE id = ?
    """, (strategy_id,))
    strategy = cursor.fetchone()

    cursor.execute(""" 
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
    """, (strategy_id,))
    stocks = cursor.fetchall()
    return templates.TemplateResponse("screener.html", {"request": request, "stocks": stocks, "strategy": strategy})
