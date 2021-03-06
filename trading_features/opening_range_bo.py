import sqlite3
import config
import smtplib, ssl
from datetime import date
from timezone import is_dst
from utils import calculate_quantity
import alpaca_trade_api as tradeapi

API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET
BASE_URL = config.BASE_URL

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute(""" 
    select id form strategy where name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute(""" 
    select symbol, name
    from stock
    join stock_strategy on stock_strategy.stock_id = stock.id
    where stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]
api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

current_date = date.today().isoformat()

if is_dst():
    start_minute_bar = f"{current_date} 9:30:00-5:00"
    end_minute_bar = f"{current_date} 9:45:00-5:00"
else:
    start_minute_bar = f"{current_date} 9:30:00-4:00"
    end_minute_bar = f"{current_date} 9:45:00-4:00"

orders = api.list_orders(status='all', limit=500, after=f"{current_date}T13:30:00Z")
existing_order_symbols = [order.symbol for order in orders if order.status != 'canceled']

#messages - []

for symbol in symbols:
    minute_bars = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from=current_date, to=current_date).df

    opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bars = minute_bars.loc[opening_range_mask]

    opening_range_low = opening_range_bars['low'].min()
    opening_range_high = opening_range_bars['high'].max()
    opening_range = opening_range_high - opening_range_low

    after_opening_range_mask = minute_bars.index >= end_minute_bar
    after_opening_range_bars = minute_bars.iloc[after_opening_range_mask]

    after_opening_range_breakout = after_opening_range_bars[after_opening_range_bars['close'] > opening_range_high]
    
    if not after_opening_range_breakout.empty:
        if symbol not in existing_order_symbols:
            limit_price = after_opening_range_breakout.iloc[0]['close']
            print(f"placing order for {symbol} at {limit_price}, closed above {opening_range_high} at {after_opening_range_bars.iloc[0]}")
            try:
                api.submit_order(
                    symbol=symbol,
                    side='buy',
                    type='limit',
                    qty=calculate_quantity(limit_price),
                    time_in_force='day',
                    order_class='bracket',
                    limit_price=limit_price,
                    take_profit=dict(
                        limit_price=limit_price+opening_range,
                    ),
                    stop_loss=dict(
                        stop_price=limit_price-opening_range,
                    )
                )
            except Exception as e:
                print(f"could not submit order {e}")
        else:
            print(f"Already an order for {symbol}, skipping")