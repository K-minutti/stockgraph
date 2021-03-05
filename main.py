from fastapi import FastAPI, Request, Form 
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
import sqlite3

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
            ) where date = ?
        """, (date.today().isoformat(),))
    elif stock_filter == 'new_closing_lows':
        cursor.execute(""" 
            select * from (
                select symbol, name, stock_id, min(close), date
                from historical_prices join stock on stock.id = historical_prices.stock_id
                group by stock_id
                order by symbol
            ) where date = ?
        """, (date.today().isoformat(),))
    else:
        cursor.execute(""" 
            select id, symbol, name from stock order by symbol
        """)
    
    rows = cursor.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})