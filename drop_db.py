import sqlite3, config

connection = sqlite3.connect(config.DB_PATH)

cursor = connection.cursor()

cursor.execute("""
    DROP TABLE historical_prices
""")

cursor.execute(""" 
    DROP TABLE stock
""")

cursor.execute(""" 
    DROP TABLE strategy
""")

cursor.execute(""" 
    DROP TABLE stock_strategy
""")

connection.commit()