import yfinance as yf
"""
    We will return the following information
    symbol -> {symbol: symbol, exchange: exchange}
    performance -> {currYear: 52Weeks, 2020, 2019...} // 5years weekly data points
    seasonality -> {Jan: .80, Feb: .80, March: .50} //max Yrs or 10Years 120 data points percentage of time the month closed higher than it opened
    Volatility -> {}
    Volume -> 
"""