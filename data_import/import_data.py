import cx_Oracle
import os 
import pandas as pd 
import sys 

if len(sys.argv) <= 3:
    print("This script takes 3 args")
    print("Arg 1 is the file name and arg 2 is whether it is gemini or bitstamp, arg 3 is btc or eth")
    sys.exit(1)



# Get environment variables
USER = os.getenv('myuser')
PASSWORD = os.getenv('mypw')
DSN = os.getenv('mydsn')

# Establish the database connection
connection = cx_Oracle.connect(user=USER, password=PASSWORD,
                               dsn=DSN)

filename = sys.argv[1]


# Read CSV data and store in lists
df = pd.read_csv(filename)

# Make a list of sequences
rows = [ (x[1],x[6],x[4],x[3],x[7],x[5] ) for x in df.values]

# Obtain a cursor
cursor = connection.cursor()

SQL = """
INSERT INTO ohlc_data_point (exchange_id, trade_date, buyer_currency, seller_currency, close, high, open, volume, low) VALUES (
    EXCHANGE_ID, -- Exchange ID
    TO_DATE(:1,'YYYY-MM-DD HH24:MI:SS'), -- date
    CURRENCY_ID , -- 1=BTC, 2=ETH
    3, -- USD
    :2, -- close 
    :3, -- high
    :4, -- open
    :5, -- volume 
    :6 -- low
)
"""



if sys.argv[2].lower() == "bitstamp":
    print("Processing bistamp file {} ".format(filename))
    SQL = SQL.replace("EXCHANGE_ID","2")
else:
    print("Processing gemini file {} ".format(filename))
    SQL = SQL.replace("EXCHANGE_ID","1")

if sys.argv[3].lower() == "eth":
    print("Setting currency_id for eth")
    SQL = SQL.replace("CURRENCY_ID","2")
else:
    print("Setting currency_id for btc")
    SQL = SQL.replace("CURRENCY_ID","1")




print("Starting the insert!")
cursor.executemany(SQL,rows)
connection.commit()

print("Done!")