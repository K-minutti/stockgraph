
def get_all_strategies(high, low, price_data):
    """
    This function takes in a high and low price as a str and price_data as sqlite row objects
    We calculate the following strategies using this data: 52 week high breakout , 52 week low breakdown, 3 bar divergence (up and down)
    """
    #first strat is price within 9% of its 52 week high ?
    #opposite as below
    #second strat is price within 9% of its 52 week low ?
    #if so then check the last 14 days if there is are lower lows and lower highs indicate strong breakdown 
    #and calc how many days it would take to see it break below the 52 week low based on the ATR 
    #for 3 bar divergence we can check are the last three bars all green ei -> closed higher then open or red ei -> closed lower than open
    #if either is true then the other isn't and we can proceed with the option that is true otherwise both are false 
    #and we can say price does not fit 3 bar divergence
    return price_data
