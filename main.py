from fastapi import FastAPI, Request, Form 
import alpaca_trade_api as tradeapi
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
import sqlite3, config

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
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
        select symbol, sma_20, sma_50, rsi_14, close
        from stock join historical_prices on historical_prices.stock_id = stock.id
        where date = (select max(date) from historical_prices)
    """)

    indicator_rows = cursor.fetchall()
    indicator_values = {}
    for row in indicator_rows:
        indicator_values[row['symbol']] = row

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows,  "indicator_values": indicator_values})


@app.get("/stock/{symbol}")
def single_stock(request: Request, symbol):
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(""" 
        SELECT * FROM strategy
    """)
    strategies = cursor.fetchall()

    cursor.execute(""" 
        SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol,))
    row = cursor.fetchone()

    cursor.execute(""" 
        SELECT * FROM historical_prices WHERE stock_id = ? ORDER BY date DESC
    """, (row['id'],))
    prices = cursor.fetchall()

    return templates.TemplateResponse("single_stock.html", {"request": request, "stock": row, "prices": prices, "strategies": strategies})

@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect('app.db')
    cursor = connection.cursor()

    cursor.execute(""" 
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?,?)
    """, (stock_id, strategy_id))

    connection.commit()
    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategies")
def strategies(request: Request):
    connection = sqlite3.connect("app.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(""" 
        select * from strategy
    """)

    strategies = cursor.fetchall()
    return templates.TemplateResponse("strategies.html", {"request" : request, "strategies": strategies})

@app.get("/orders")
def orders(request: Request):
    api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)
    orders = api.list_orders(status="all")
    return templates.TemplateResponse("orders.html", {"request" :request, "orders": orders})


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
    return templates.TemplateResponse("strategy.html", {"request": request, "stocks": stocks, "strategy": strategy})