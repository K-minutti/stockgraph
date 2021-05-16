import sqlite3, config
import numpy as np
import tulipy as ti
import alpaca_trade_api as tradeapi
from datetime import date, timedelta


API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET
BASE_URL = config.BASE_URL

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute(""" 
    SELECT id, symbol, name FROM stock
""")

rows = cursor.fetchall()

#we need to be able to run this script every day of the week.

symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)
#limit per alpaca
chunk_size = 200
yesterday = date.today() - timedelta(days=1)
for i in range(0, len(symbols), chunk_size):
    symbol_chunk = symbols[i:i+chunk_size]
    #after=date.today().isoformat()

    barsets = api.get_barset(symbol_chunk, 'day', limit=60)
    
    for symbol in barsets:

        recent_closes = [bar.c for bar in barsets[symbol]]
        recent_highs = [bar.h for bar in barsets[symbol]]
        recent_lows = [bar.l for bar in barsets[symbol]]
        print(f"processing symbol {symbol}")
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol]
            #if len(recent_closes) >= 50 and date.today().isoformat() == bar.t.date().isoformat():
            if len(recent_closes) >= 50 and yesterday.isoformat() == bar.t.date().isoformat():
                sma_20 = ti.sma(np.array(recent_closes), period=20)[-1]
                sma_50 = ti.sma(np.array(recent_closes), period=50)[-1]
                rsi_14 = ti.rsi(np.array(recent_closes), period=14)[-1]
                atr_14 = ti.atr(np.array(recent_highs), np.array(recent_lows), np.array(recent_closes), period=14)[-1]
                change = (recent_closes[-1] - recent_closes[-2]) / recent_closes[-2] * 100
            else:
                sma_20, sma_50, rsi_14, atr_14, change = None, None, None, None, None
            print(f"{symbol} {sma_20} {sma_50} {rsi_14} {atr_14} {change}")
            cursor.execute(""" 
                INSERT INTO historical_prices (stock_id, date, open, high, low, close, volume, change, sma_20, sma_50, rsi_14)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, change, sma_20, sma_50, rsi_14))

connection.commit() 