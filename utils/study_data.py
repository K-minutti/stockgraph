import yfinance as yf
from datetime import date
import numpy as np

#MAIN- FUNCTION
def compute_study_data(symbol):
    daily_3M, weekly_5Y, monthly_10Y = get_time_series_data(symbol)
    performance = get_performance(weekly_5Y)
    seasonality = get_seasonality(monthly_10Y)
    return seasonality


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

def get_volatility(data):
    """
    https://www.tradingview.com/lightweight-charts/
    
    Volatility -> {} // Plot 5 period ATR Of Weekly - 5Y chart , Plot 14 period ATR Of daily - 3m chart, variance and stddev | for each chart plotted plot price line as well 
    df create ATR5 Col fror Weekly5Y data and and ATR14 Col for Daily3M  same for variance col and stddev col
    https://tulipindicators.org/var
    https://tulipindicators.org/stddev
    
    """
    pass

def get_volume_analysis(data):
    """
    Volume -> {} //  take volume over last 3 months and identify any volume spikes, periods of largest volume and plot horizontal lines on tops/ bottoms of those candels
    is stock in a low volume period ? or high volume period.

    """
    pass


print(compute_study_data("TSLA"))





















#STOP THIS FILE IS GETTING LONG