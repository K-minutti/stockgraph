
"""
@/Screener 
Dict for SQL calls by filter option
"""
db_calls = {
    "greater_than_3%": "change > 3",
    "greater_than_6%": "change > 6",
    "greater_than_10%": "change > 10",
    "greater_than_15%": "change > 15",
    "greater_than_20%": "change > 20",
    "greater_than_25%": "change > 25",
    "greater_than_30%": "change > 30",
    "less_than_-3%": "change < -3",
    "less_than_-6%": "change < -6",
    "less_than_-10%": "change < -10",
    "less_than_-15%": "change < -15",
    "less_than_100000": "volume < 100000",
    "less_than_1000000": "volume < 1000000",
    "greater_than_100000": "volume > 100000",
    "greater_than_250000": "volume > 250000",
    "greater_than_500000": "volume > 500000",
    "greater_than_1000000": "volume > 1000000",
    "greater_than_3000000": "volume > 3000000",
    "greater_than_6000000": "volume > 6000000",
    "greater_than_10000000": "volume > 10000000",
    "under_sma_50": "close < sma_50",
    "under_equal_sma_50": "close <= sma_50",
    "over_sma_50": "close > sma_50",
    "over_equal_sma_50": "close >= sma_50",
    "under_sma_20": "close < sma_20",
    "under_equal_sma_20": "close <= sma_20",
    "over_sma_20": "close > sma_20",
    "over_equal_sma_20": "close >= sma_20",
    "rsi_overbought" : "rsi_14 > 70",
    "rsi_oversold" : "rsi_14 < 30"
    }