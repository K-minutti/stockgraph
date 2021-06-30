import yfinance as yf

#TODO: ADD 52-WEEK HIGH AND LOW to company_data

def get_company_data(symbol):
    company_data = {
        'info': {
            'city':"-", 
            'country':"-", 
            'floatShares':"-", 
            'industry':"-", 
            'longBusinessSummary': "-", 
            'marketCap': "-", 
            'sector':"-", 
            'sharesOutstanding':"-", 
            'sharesShort':"-", 
            'state':"-", 
            'website':"-"
        },
        'ratings' : {'valid': False, 'data': []}
    }

    symbol_data = yf.Ticker(symbol)
    try: 
        data = symbol_data.recommendations
        data = data.reset_index()
        data = data.iloc[::-1]
        ratings = data.to_dict('records')
        company_data['ratings']['valid'] = True
        company_data['ratings']['data'] = ratings[:10] 
        for rating in company_data['ratings']['data']:
            rating['Date'] = rating['Date'].strftime("%m-%d-%Y")
            if rating['From Grade'] == "":
                rating['From Grade'] = "-"
    except Exception as error:
        print(error)
    
    for key in company_data['info']:
        info =  symbol_data.info
        try:
            company_data['info'][key] = info[key]
        except Exception as error:
            print(f"Issue with key : {key}. For symbol {symbol}. Error: {error}")

    return company_data

