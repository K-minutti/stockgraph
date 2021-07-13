import yfinance as yf

daily_data_3M = yf.download(tickers="PLTR", period="3mo", interval="1d") #60~ data points
weekly_data_5Y = yf.download(tickers="PLTR", period="5y", interval="1wk") #250~ data points
monthly_data_10Y = yf.download(tickers="PLTR", period="10y", interval="1mo") #120~ data points

print("\n" , "DAILY")
print(daily_data_3M.head())
print("\n" , "WEEKLY")
print(weekly_data_5Y.head())
print("\n",  "MONTHLY")
print(monthly_data_10Y.head())
"""
    performance -> {currYear: 52Weeks, 2020, 2019...} // 5years weekly data points 5 x 50 250 or so data points

    seasonality -> {Jan: .80, Feb: .80, March: .50} //max Yrs or 10Years 120 data points percentage of time the month closed higher than it opened
    Volatility -> {} // Plot 5 period ATR Of Weekly - 5Y chart , Plot 14 period ATR Of daily - 3m chart, variance and stddev | for each chart plotted plot price line as well 
    Volume -> {} //  take volume over last 3 months and identify any volume spikes, periods of largest volume and plot horizontal lines on tops/ bottoms of those candels
    is stock in a low volume period ? or high volume period.
"""