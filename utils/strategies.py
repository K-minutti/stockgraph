import math
import numpy as np
import pandas as pd

def get_all_strategies(high, low, price_data):
    """
    This function takes in a high and low price as a str and price_data as a pandas dataframe
    We calculate the following strategies using this data: 52 week high breakout , 52 week low breakdown, 3 bar divergence (up and down)
    """
    #return values
    output = {
        "breakout": "- n/a -", 
        "breakdown": "- n/a -", 
        "strategy_one_message": "- none -",
        "threebar_up": "- n/a -", 
        "threebar_down": "- n/a -", 
        "strategy_two_message": "- none -"
    }

    #Getting ATR
    high_low = price_data['high'] - price_data['low']
    high_close = np.abs(price_data['high'] - price_data['close'].shift())
    low_close = np.abs(price_data['low'] - price_data['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr_values = true_range.rolling(14).sum()/14
    atr_list = atr_values.tolist()

    atr = atr_list[-1]
    last = price_data.iloc[-1]['close']
    upper_limit, lower_limit = calculate_thresholds(high, low)

    #Strategy 1 - 52 Week Breakout and Breakdown
    if last > lower_limit and last < upper_limit:
        output['strategy_one_message'] = "No 52 week high breakout or 52 week low breakdown likely at the moment."
    if last < lower_limit:
        days = atr_price_action(last, low, atr)
        output['breakdown']  = f"It would take about {days} day(s) for price to break below the 52 week low of {low:.2f} based on the 14-Day ATR of {atr:.2f} in the best case scenario."
    if last > upper_limit:
        days = atr_price_action(last, low, atr)
        output['breakout'] = f"It would take about {days} day(s) for price to break above the 52 week high of {high:.2f} based on the 14-Day  ATR of {atr:.2f} in the best case scenario."
    

    price_data_last_3 = price_data[['open', 'close']].tail(3)
    price_data_last_3['all_closed_higher'] = price_data_last_3['open'] < price_data_last_3['close']
    all_higher = price_data_last_3['all_closed_higher'].eq(True).all()
    all_lower = price_data_last_3['all_closed_higher'].eq(False).all()
    if all_higher:
        output['threebar_up'] = 'The last three days have closed higher than the same day\'s open. There is potential for a downside divergence on the next trading day.'
    if all_lower:
        output['threebar_down'] = 'The last three days have closed lower than the same day\'s open. There is potential for an upside divergence on the next trading day.'
    if all_higher == False and all_lower == False:
        output['strategy_two_message'] = 'Price has not been trending for the past three days. Divergence not possible.'

    return output

def calculate_thresholds(high, low):
    #returns price thresholds to check the last price against to confirm if its within 52W high or low
    range = high - low
    ten_percent = range * .11
    upper_limit = high - ten_percent
    lower_limit = low + ten_percent
    return upper_limit, lower_limit

def atr_price_action(start, target, atr):
    if target > start:
        delta = target - start 
        days = math.ceil(delta/atr)
        return days
    if target < start:
        delta = start - target
        days = math.ceil(delta/atr)
        return days


