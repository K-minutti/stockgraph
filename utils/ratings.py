import yfinance as yf

def get_ratings(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.recommendations
    if data.empty:
        return None
    else:
        data = data.reset_index()
        data.iloc[::-1]
        ratings = data.to_dict('records')
        return ratings


#OUTPUT : [{'Date': Timestamp('2021-05-12 12:31:45'), 'Firm': 'Roth Capital', 'To Grade': 'Buy', 'From Grade': '', 'Action': 'main'}...]
