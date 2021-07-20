import yfinance as yf
from datetime import date
import tulipy as ti
import numpy as np
import pandas as pd

#MAIN- FUNCTION
def compute_study_data(symbol):
    daily_3M, weekly_5Y, monthly_10Y = get_time_series_data(symbol)
    performance = get_performance(weekly_5Y)
    seasonality = get_seasonality(monthly_10Y)
    volatility = get_volatility(weekly_5Y, 5)
    volume_analysis = get_volume_analysis(daily_3M)
    return {"performance":performance, "seasonality": seasonality, "volatility": volatility, "volume_analysis": volume_analysis}


def get_time_series_data(symbol):
    daily_data_3M = yf.download(symbol, period="3mo", interval="1d") #60~ data points
    weekly_data_5Y =  yf.download(symbol, period="5y", interval="1wk") #250~ data points
    monthly_data_10Y =  yf.download(symbol, period="10y", interval="1mo") #120~ data points
    return daily_data_3M, weekly_data_5Y, monthly_data_10Y

#PERFORMANCE FUNC
def get_performance(data):
    processed_data = process_data_for_performance(data)
    performance_by_year = get_performance_by_year(processed_data)
    return performance_by_year

#Helper  - @get_performance
def process_data_for_performance(data):
    data.dropna(subset=['Close'], inplace=True) #Any row that has missing price info is dropped
    data = data.fillna(0)
    return data

def get_five_years():
    curr_year = date.today().year
    years = [x for x in range(curr_year, curr_year-5, -1)]
    return years

#Helper  - @get_performance  
def get_performance_by_year(data):
    performance_by_year = {}
    last_five_years = get_five_years()
    for year in last_five_years:
        year_df = data[data.index.year == year].copy()
        year_df['time'] = [f"{last_five_years[0]}-{x.month}-{x.day}" for x in year_df.index] 
        year_df.rename(columns={'Close': 'value'}, inplace=True)
        year_df = year_df.drop(columns=['Open', 'High', 'Low', 'Adj Close', 'Volume'])
        performance_by_year[year] = year_df.to_dict('records')
    return performance_by_year


#SEASONALITY FUNC
def get_seasonality(data):
    months = [x for x in range(1,13)]
    seasonality_by_month = {"months":[], "value":[]}

    for month in months:
        monthly_data = data[data.index.month == month].copy()
        total_months = len(monthly_data)
        open_less_than_close_df = monthly_data[monthly_data['Open'] < monthly_data['Close']]
        months_closed_higher = len(open_less_than_close_df)
        percentage_of_months_closed_higher = months_closed_higher / total_months
        seasonality_by_month["months"].append(month)
        seasonality_by_month["value"].append(percentage_of_months_closed_higher)
        #seasonality_by_month.append({'time': month, 'value': percentage_of_months_closed_higher}) #TV record format
    return seasonality_by_month


#VOLATILITY ANALYSIS
def get_volatility(data, period):
    """ period : int used as calulcation period for atr, variance, and stddev"""
    highs, lows, closes = hlc_series(data)
    atr_series = ti.atr(highs, lows, closes, period=period)
    variance_series = ti.var(closes, period=period)
    stddev_series = ti.stddev(closes, period=period)
    series_start = len(data) - len(atr_series)
    df_with_series =  data.iloc[series_start::].copy()
    df_with_series['ATR'] = atr_series
    df_with_series['Variance'] = variance_series
    df_with_series['StdDev'] = stddev_series
    df_with_series['time'] = [f"{x.year}-{x.month}-{x.day}" for x in df_with_series.index] 
    atr_plot = convert_series_to_dictrows(df_with_series, 'ATR')
    variance_plot = convert_series_to_dictrows(df_with_series, 'Variance')
    stddev_plot = convert_series_to_dictrows(df_with_series, 'StdDev')
    return {"atr": atr_plot, "variance":variance_plot,"stddev" : stddev_plot}

def hlc_series(data):
    highs = data['High'].to_numpy()
    lows = data['Low'].to_numpy()
    closes = data['Close'].to_numpy()
    return highs, lows, closes


def convert_series_to_dictrows(data, col):
    subset = data[["time", f"{col}"]]
    subset.rename(columns={f"{col}": "value"}, inplace=True)
    return subset.to_dict('records')


#VOLUME ANALYSIS
#Helper for @get_volume_analysis
def set_color(row):
    if row['Volume_Ratio'] > 2.5:
        return 'rgb(106, 90, 205, 0.9)'
    if row['Open'] < row['Close'] :
        return 'rgba(0, 150, 136, 0.8)'
    else:
        return 'rgba(255,82,82, 0.8)' 

def get_volume_analysis(data):
    data['Volume_Ratio'] = data['Volume'] / data['Volume'].shift(+1)
    data['color'] = data.apply(lambda row: set_color(row), axis=1)
    data['time'] = [f"{x.year}-{x.month}-{x.day}" for x in data.index] 
    volume_spikes = data[data['Volume_Ratio']> 2.5]
    volume_spikes = volume_spikes[['time', 'Close']]
    volume_spikes.rename(columns={'Close':'price'}, inplace=True)
    volume_spikes = volume_spikes.to_dict('records')
    volume_data = data[['time', 'Volume', 'color']]
    volume_data.rename(columns={'Volume': 'value'}, inplace=True)
    volume_data = volume_data.to_dict('records')
    return {"horizontal-prices": volume_spikes, "volume" :volume_data}


#print(compute_study_data("APT"))
