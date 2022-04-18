import pandas as pd 

df = pd.read_csv("data/Bitstamp_BTCUSD_2018_minute.csv")
unix = df['unix'].tolist()
date = df['date'].tolist()
symbol = df['symbol'].tolist()
open = df['open'].tolist()
high = df['high'].tolist()
low = df['low'].tolist()
close = df['close'].tolist()
volume = df['Volume BTC'].tolist()


INSERT_DATA_SQL = """
INSERT INTO ohlc_data_point (exchange_id, trade_date, buyer_currency, seller_currency, close, high, open, volume, low) VALUES (
    1, -- Gemini
    TO_DATE(:1,'YYYY-MM-DD HH24:MI:SS'), -- date
    1, -- BTC 
    2, -- ETH
    :2, -- close 
    :3, -- high
    :4, -- open
    :5, -- volume 
    :6 -- low
)
""" 

rows = [ (x[1],x[6],x[4],x[3],x[7],x[5] ) for x in df.values]

print(type(date[0]))
print("TEST")
print("TEST")