import yfinance as yf
from datetime import date
import numpy as np

#MAIN- FUNCTION
def compute_study_data(symbol):
    daily_3M, weekly_5Y, monthly_10Y = get_time_series_data(symbol)
    performance = get_performance(weekly_5Y)
    return performance


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
    data['Change'] = data['Close'].pct_change()
    data.dropna(subset=['Close'], inplace=True) #Any row that has missing price info is dropped
    data = data.drop(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    data = data.fillna(0)
    return data

def get_performance_by_year(data):
    performance_by_year = {}
    last_five_years = get_five_years()
    for year in last_five_years:
        year_df = data[data.index.year == year]
        year_df['Week'] = np.arange(1, len(year_df)+1)
        performance_by_year[year] = year_df.to_dict('records')
    return performance_by_year

#Helper  - @get_performance    
def get_five_years():
    curr_year = date.today().year
    years = [x for x in range(curr_year, curr_year-5, -1)]
    return years

def get_seasonality(data):
    """
    calc percentage of time price closed higher then it opened for every month for all years
     seasonality -> {Jan: .80, Feb: .80, March: .50} // return object with 12 key-value pairs where each month holds a percentage 
       df create month col group by month then group by month then return new df where each row is a month and each month has a percentage col and calc 
       X / total where X is total num of rows where row.open < row.close and total is the total nums of monthly data points in each group
    """
    pass

def get_volatility(data):
    """
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


print(compute_study_data("AAPL"))





















#STOP THIS FILE IS GETTING LONG