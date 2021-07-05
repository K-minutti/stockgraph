import math
import numpy as np
import pandas as pd

def get_all_strategies(high, low, price_data):
    """
    This function takes in a high and low price as a str and price_data as a pandas dataframe
    We calculate the following strategies using this data: 52 week high breakout , 52 week low breakdown, 3 bar divergence (up and down)
    """

    high_low = price_data['high'] - price_data['low']
    high_close = np.abs(price_data['high'] - price_data['close'].shift())
    low_close = np.abs(price_data['low'] - price_data['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr_values = true_range.rolling(14).sum()/14
    atr_list = atr_values.tolist()
    atr = atr_list[-1]
    last = price_data.iloc[-1]['close']
    message = ""

    return atr, last

'''
    upper_limit, lower_limit = calculate_thresholds(high, low)

    if last > lower_limit and last < upper_limit:
        message = "No 52 week high breakout or 52 week low breakdown likely at the moment."
    if last < lower_limit:
        days = atr_price_action(last, low, atr)
        message = f"It would take about {days} for price to break below the 52 week high of {low} based on the 14-Day {atr} in the best case scenario."
    if last > upper_limit:
        days = atr_price_action(last, low, atr)
        message = f"It would take about {days} for price to break above the 52 week low of {high} based on the 14-Day {atr} in the best case scenario."
    #----
    #for 3 bar divergence we can check are the last three bars all green ei -> closed higher then open or red ei -> closed lower than open
    #if either is true then the other isn't and we can proceed with the option that is true otherwise both are false 
    #and we can say price does not fit 3 bar divergence
    return price_data

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



'''