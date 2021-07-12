from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

data = pdr.get_data_yahoo("SPY", start="2017-01-01", end="2017-04-30")
"""
    performance -> {currYear: 52Weeks, 2020, 2019...} // 5years weekly data points
    seasonality -> {Jan: .80, Feb: .80, March: .50} //max Yrs or 10Years 120 data points percentage of time the month closed higher than it opened
    Volatility -> {}
    Volume -> 
"""



print(data)