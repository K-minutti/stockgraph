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
    volatility = get_volatility(weekly_5Y, daily_3M)
    return volatility


def get_time_series_data(symbol):
    daily_data_3M = yf.download(symbol, period="3mo", interval="1d") #60~ data points
    weekly_data_5Y =  yf.download(symbol, period="5y", interval="1wk") #250~ data points
    monthly_data_10Y =  yf.download(symbol, period="10y", interval="1mo") #120~ data points
    return daily_data_3M, weekly_data_5Y, monthly_data_10Y


def get_performance(data):
    processed_data = process_data_for_performance(data)
    performance_by_year = get_performance_by_year(processed_data)
    return performance_by_year

#Helper  - @get_performance
def process_data_for_performance(data):
    data['value'] = data['Close'].pct_change()
    data.dropna(subset=['Close'], inplace=True) #Any row that has missing price info is dropped
    data = data.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    data = data.fillna(0)
    return data

#Helper  - @get_performance  
def get_performance_by_year(data):
    performance_by_year = {}
    last_five_years = get_five_years()
    for year in last_five_years:
        year_df = data[data.index.year == year].copy()
        year_df['time'] = np.arange(1, len(year_df)+1)
        performance_by_year[year] = year_df.to_dict('records')
    return performance_by_year

def get_five_years():
    curr_year = date.today().year
    years = [x for x in range(curr_year, curr_year-5, -1)]
    return years


def get_seasonality(data):
    months = [x for x in range(1,13)]
    seasonality_by_month = []
    for month in months:
        monthly_data = data[data.index.month == month].copy()
        total_months = len(monthly_data)
        open_less_than_close_df = monthly_data[monthly_data['Open'] < monthly_data['Close']]
        months_closed_higher = len(open_less_than_close_df)
        percentage_of_months_closed_higher = months_closed_higher / total_months
        seasonality_by_month.append({'time': month, 'value': percentage_of_months_closed_higher})
    return seasonality_by_month

def get_volatility(weeklyData, dailyData):
    """>  {'time', 'value'}"""
    hi = atr_series(dailyData, 7)
    return hi

def atr_series(data, period=14):
    highs = data['High'].to_numpy()
    lows = data['Low'].to_numpy()
    closes = data['Close'].to_numpy()
    atr_series = ti.atr(highs, lows, closes, period=period) #mask the data for the date starting from 
    variance_series = ti.var(closes, period=period)
    stddev_series = ti.stddev(closes, period=period)
    series_start = len(data) - len(atr_series)
    df_with_series =  data.iloc[series_start::].copy()
    df_with_series['ATR'] = atr_series
    df_with_series['Variance'] = variance_series
    df_with_series['STD_Dev'] = stddev_series  # age_sex = titanic[["Age", "Sex"]]
    df_with_series['time'] = [f"{x.year}-{x.month}-{x.day}" for x in df_with_series.index] 
    atr_ = df_with_series[["time", "ATR"]]
    atr_.rename(columns={'ATR': 'value'}, inplace=True) #orders.rename(columns={'Order_Date' :'Date'},inplace=True)
    atr_ = atr_.to_dict('records')
    return  atr_
    

def get_volume_analysis(data):
    """
    Volume -> {} //  take volume over last 3 months and identify any volume spikes, periods of largest volume and plot horizontal lines on tops/ bottoms of those candels
    is stock in a low volume period ? or high volume period.

    """
    pass


print(compute_study_data("BTU"))
#STOP THIS FILE IS GETTING LONG