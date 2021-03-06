import config
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.BASE_URL)

response = api.close_all_positions()

print(response)
#set crontab job