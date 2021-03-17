import config 
import tulipy as ti
from utils import calculate_quantity
import alpaca_trade_api as tradeapi


API_KEY = config.API_KEY
SECRET_KEY = config.API_SECRET
BASE_URL = config.BASE_URL

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

symbols = []

for symbol in symbols:
    quote = api.get_last_quote(symbol)
    api.submit_order(
        symbol=symbol,
        side="buy",
        type="market",
        qty=calculate_quantity(quote.bidprice),
        time_in_force="day"
    )



orders = api.list_orders()
positions = api.list_positions()

# api.submit_order(
#     symbol=symbol,
#     side='sell',
#     qty=arb,
#     time_in_force="day",
#     type="trailing_stop",
#     trail_price="0.20",
# )

# api.submit_order(
#     symbol=symbol,
#     side='sell',
#     qty=arb,
#     time_in_force="day",
#     type="trailing_stop",
#     trail_percent="0.20",
# )


# daily_bars = api.polygon.historic_agg_v2('NIO', 1, 'day', _from='date', to='date').df

#atr = ti.atr(daily_bars.high.values, daily_bars.low.values, daily_bars.close.values, 14)