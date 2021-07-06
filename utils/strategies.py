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
        "breakout": "-", 
        "breakdown": "-", 
        "strategy_one_message": "-",
        "threebar_up": "-", 
        "threebar_down": "-", 
        "strategy_two_message": "-"
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
        output['breakdown']  = f"It would take about {days} for price to break below the 52 week high of {low} based on the 14-Day {atr} in the best case scenario."
    if last > upper_limit:
        days = atr_price_action(last, low, atr)
        output['breakout'] = f"It would take about {days} for price to break above the 52 week low of {high} based on the 14-Day {atr} in the best case scenario."
    
    #Strategy 2 - 3 Bar Divergence 
    #----
    #get the last three opens
    #get the last three close
    #if all the open are greater than the open then we can check that the last days highest high is higher than the third days low 
    #if they criteria fits then we can label it as a potential divergence given the last three days 
    #last_three_days = 
    #do the opposite for the upside divergence


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


