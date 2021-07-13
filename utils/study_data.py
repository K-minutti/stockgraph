import yfinance as yf


def compute_study_data(symbol):
    daily_data_3M, weekly_data_5Y, monthly_data_10Y = get_time_series_data(symbol)
    pass

def get_time_series_data(symbol):
    daily_data_3M = yf.download(symbol, period="3mo", interval="1d") #60~ data points
    weekly_data_5Y =  yf.download(symbol, period="5y", interval="1wk") #250~ data points
    monthly_data_10Y =  yf.download(symbol, period="10y", interval="1mo") #120~ data points
    return daily_data_3M, weekly_data_5Y, monthly_data_10Y

def get_performance(data):
    """
    return an object with keys for every year that hold values equal to an object of records where we have  {year: {date: 1, change: "",})
    and the date corresponds to a week of data so 1 is the first week of january for any given year
    """
    pass

def get_seasonality(data):
    """
    calc percentage of time price closed higher then it opened for every month for all years
     seasonality -> {{Jan: .80, Feb: .80, March: .50} // return object with 12 key-value pairs where each month holds a percentage 
       df create month col group by month then group by month then return new df where each row is a month and each month has a percentage col and calc 
       X / total where X is total num of rows where row.open < row.close and total is the total nums of monthly data points in each group
    """
    pass

def get_volatility(data):
    """
    Volatility -> {} // Plot 5 period ATR Of Weekly - 5Y chart , Plot 14 period ATR Of daily - 3m chart, variance and stddev | for each chart plotted plot price line as well 
    df create ATR5 Col fror Weekly5Y data and and ATR14 Col for Daily3M  same for variance col and stddev col
    """
    pass

def get_volume_analysis(data):
    """
    Volume -> {} //  take volume over last 3 months and identify any volume spikes, periods of largest volume and plot horizontal lines on tops/ bottoms of those candels
    is stock in a low volume period ? or high volume period.
    
    """
    pass
compute_study_data("AAPL")