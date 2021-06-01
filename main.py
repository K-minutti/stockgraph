from fastapi import FastAPI, Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from numpy.lib.twodim_base import diag
import pandas as pd
import datetime
import time
import requests
import sqlite3
from utils import api_utils as utils
from trading_features import ratings
import alpaca_trade_api as tradeapi
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

    #grabbing top gainers
    cursor.execute(""" 
        SELECT stock_id, change FROM historical_prices WHERE change IS NOT NULL ORDER BY change DESC LIMIT 10
    """)
    gainers = cursor.fetchall()
    #grabbing top decliners
    cursor.execute(""" 
        SELECT stock_id, change FROM historical_prices WHERE change IS NOT NULL ORDER BY change ASC LIMIT 10
    """)
    decliners = cursor.fetchall()
    top_gainers = []
    top_decliners = []
    for stock in gainers:
      cursor.execute(""" 
           SELECT symbol FROM stock WHERE id IS ?
      """,(stock['stock_id'],))
      symbol = cursor.fetchone()
      top_gainers.append({"symbol": symbol['symbol'], "change": round(stock['change'], 2)})
    
    for stock in decliners:
      cursor.execute(""" 
           SELECT symbol FROM stock WHERE id IS ?
      """,(stock['stock_id'],))
      symbol = cursor.fetchone()
      top_decliners.append({"symbol": symbol['symbol'], "change": round(stock['change'], 2)})
    
    top_stocks = []
    #grouping top stocks
    for gainer, decliner in zip(top_gainers, top_decliners):
        top_stocks.append((gainer, decliner))

    # get the advance /decline
    cursor.execute(""" 
        SELECT COUNT(change) FROM historical_prices WHERE change>0
    """)
    advancers_count = cursor.fetchone()
    cursor.execute(""" 
        SELECT COUNT(change) FROM historical_prices WHERE change<0
    """)
    decliners_count = cursor.fetchone()
    cursor.execute(""" 
        SELECT COUNT(change) FROM historical_prices WHERE change=0
    """)
    neutral_count = cursor.fetchone()
    #.isoformat()
    #for stocks in indices fetch the historical data by id 
    indices = {"SPY": [], "QQQ": [], "DIA": [], "IWM": []}
    index_ids = {10: "SPY", 5424:"QQQ", 50:"DIA", 3499:"IWM"}
    for key in index_ids:
        cursor.execute(""" 
            SELECT date, close FROM historical_prices WHERE stock_id IS ? ORDER BY date DESC LIMIT 21
        """, (key,))
        stock_index_data = cursor.fetchall()
        length = len(stock_index_data) - 1
        for i in range(length, 0, -1):
            indices[index_ids[key]].append({'time': stock_index_data[i]['date'], 'value': stock_index_data[i]['close']}) 
    spy = indices['SPY']
    qqq = indices['QQQ']
    dia = indices['DIA']
    iwm = indices['IWM']
    #"all_stocks": all_stocks
    return templates.TemplateResponse("index.html", {"request": request,"top_stocks": top_stocks,  "news": all_news, "g_trends":google_trends, "ad_data": [decliners_count[0], neutral_count[0], advancers_count[0]], "spy": spy, "qqq": qqq,"dia": dia, "iwm": iwm})





@app.get("/search/{query_str}")
async def search_stock(query_str: str):
    query = query_str + '%'
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT symbol, name, exchange FROM stock WHERE symbol LIKE ? OR name LIKE ? LIMIT 30
    """,(query,query))
    search_results = cursor.fetchall()
    return {"results": search_results, "res": query_str}


@app.get("/stock/{symbol}")
def single_stock(request: Request, symbol):

    #Ratings for sidebar
    #webscrapping module

    search = gn.search(f'NASDAQ:{symbol}', when = '6m') #for symbol stock.exchange:symbol, stock.name
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
    #2021-05-27T12:24:08Z
    stock_twits = twits['messages']
    for twit in stock_twits:
        day_f = datetime.datetime.strptime(twit['created_at'],"%Y-%m-%dT%H:%M:%SZ")
        day_f.strftime("%Y-%m-%d %H:%M")
        twit['created_at'] = day_f 

    stock = {"symbol": symbol, "name": symbol}
    return templates.TemplateResponse("single_stock.html", {"request": request, "stock": stock, "news":news, "stock_twits": stock_twits})



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
    change_filter = request.query_params.get('change', False )
    volume_filter = request.query_params.get('volume', False )
    high_low_filter = request.query_params.get('high_low', False )
    sma50_filter = request.query_params.get('sma50', False )
    sma20_filter = request.query_params.get('sma20', False )
    rsi_filter = request.query_params.get('rsi', False )
    #[change_filter, volume_filter, high_low_filter, sma50_filter, sma20_filter, rsi_filter]
    #filter_statements = []
    #for filter in filters:
    #   if filter:
    #       filter_statements.append(valid_queries[filter])
    #
    #
    #for statement in filter_statements 
    #join with " AND "
    #
    #column operator threshold 
    #
    print("HEY THIS IS IT-->", utils.db_calls['greater_than_3%'])
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if high_low_filter == 'new_closing_highs':
        cursor.execute(""" 
            select * from (
                select symbol, name, stock_id, max(close), date
                from historical_prices join stock on stock.id = historical_prices.stock_id
                group by stock_id
                order by symbol
            ) where date = (select max(date) from historical_prices)
        """)
    elif high_low_filter == 'new_closing_lows':
        cursor.execute(""" 
            select * from (
                select symbol, name, stock_id, min(close), date
                from historical_prices join stock on stock.id = historical_prices.stock_id
                group by stock_id
                order by symbol
            ) where date = (select max(date) from historical_prices)
        """)
    # elif stock_filter == 'rsi_overbought':
    #     cursor.execute(""" 
    #         select symbol, name, stock_id, date
    #         from historical_prices join stock on stock.id = historical_prices.stock_id
    #         where rsi_14 > 70
    #         AND date = (select max(date) from historical_prices)
    #         order by rsi_14 desc
    #     """)
    # elif stock_filter == 'rsi_oversold':
    #     cursor.execute(""" 
    #         select symbol, name, stock_id, date
    #         from historical_prices join stock on stock.id = historical_prices.stock_id
    #         where rsi_14 < 30
    #         AND date = (select max(date) from historical_prices)
    #         order by rsi_14 asc
    #     """)
    # elif stock_filter == 'under_sma_50':
    #     cursor.execute(""" 
    #         select symbol, name, stock_id, date
    #         from historical_prices join stock on stock.id = historical_prices.stock_id
    #         where close < sma_50
    #         AND date = (select max(date) from historical_prices)
    #         order by symbol
    #     """)
    # elif stock_filter == 'over_sma_50':
    #     cursor.execute(""" 
    #         select symbol, name, stock_id, date
    #         from historical_prices join stock on stock.id = historical_prices.stock_id
    #         where close > sma_50
    #         AND date = (select max(date) from historical_prices)
    #         order by symbol
    #     """)
    else:
        cursor.execute(""" 
                select id, symbol, name from stock order by symbol
            """)
    rows = cursor.fetchall()

    cursor.execute(""" 
        select symbol, sma_20, sma_50, rsi_14, close
        from stock join historical_prices on historical_prices.stock_id = stock.id
        where date = (select max(date) from historical_prices)
    """)
    indicator_rows = cursor.fetchall()
    indicator_values = {}
    for row in indicator_rows:
        indicator_values[row['symbol']] = row


    return templates.TemplateResponse("screener.html", {"request" : request, "stocks": rows,  "indicator_values":indicator_values})

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
  