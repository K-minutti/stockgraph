import yfinance as yf

def get_ratings(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.recommendations
    try: 
        data = data.reset_index()
        data.iloc[::-1]
        ratings = data.to_dict('records')
        return ratings
    except Exception as error:
        print(error)
        return None

#OUTPUT : [{'Date': Timestamp('2021-05-12 12:31:45'), 'Firm': 'Roth Capital', 'To Grade': 'Buy', 'From Grade': '', 'Action': 'main'}...]
