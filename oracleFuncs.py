from datetime import datetime
import cx_Oracle
import os 
import sys 
from decouple import config
from re import search

# Numeric Constants for Currency Types 
BTC=1
ETH=2
USD=3

#Numeric Constants for Exchanges
GEMINI=1
BITSTAMP=2


#Class that will be used as the return value of the Query Functions. It returns up to 3 lists of values
class queryResult():
    A = list()
    B = list()
    C = list()

def getConnection() -> cx_Oracle.Connection: 
    # Get config info from .env file
    USER = config('myuser')
    PASSWORD = config('mypw')
    DSN = config('mydsn')
    DEBUG = config('DEBUG', default=False, cast=bool)
  
    #Modify the path variable to contain instant client DLLs
    if search("instantclient-basic-windows.x64-21.3.0.0.0", os.environ["PATH"]):
        if DEBUG:
            print("Instant client in PATH, doing nothing")
    else:
        if DEBUG:
            print("Instant client NOT found in PATH variable... Attempting to set it manually")
        
        currentPath= os.environ["PATH"]
        os.environ["PATH"] = "{};{}".format(".\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3",currentPath) 

    return cx_Oracle.connect(user=USER, password=PASSWORD,dsn=DSN)

def testConnection():
    with getConnection() as connection:
        SQL = """
        select 'it works' from dual
        """
        # Obtain a cursor
        cursor = connection.cursor()
        
        rows = cursor.execute(SQL)
        for x in rows:
            print(x)

def queryOne(buyerCurrencyID:int, exchangeID: int, startDate: datetime, endDate: datetime) -> queryResult:

    SQL = """
    SELECT trade_date,open,
       - 100.0 * (1 - LEAD(open) OVER (ORDER BY trade_date) / open) AS Percent_Change
    FROM KEREKOVSKIK.OHLC_DATA_POINT
    WHERE buyer_currency =:1 AND exchange_id = :2
    AND trade_date between :3 and :4
    ORDER BY trade_date ASC
    """

    result: queryResult = queryResult()

    with getConnection() as connection:
        with connection.cursor() as cursor:
            resultSet = cursor.execute(SQL,(buyerCurrencyID,exchangeID,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                result.B.append(row[1])
                result.C.append(row[2])
                #print(row)

    return result


def testQueryOne():

    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 1, 1, 0, 0, 0, 0)
    end = datetime(2018, 1, 14, 0, 0, 0, 0)
    myresult = queryOne(BTC,GEMINI,start, end)

def queryFour(buyerCurrencyID:int, exchangeID: int, startDate: datetime, endDate: datetime) -> queryResult:

    SQL = """
        SELECT TRADE_DATE, BUYER_CURRENCY,VOLUME
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = :1 AND EXCHANGE_ID = :2
        AND trade_date between :3 and :4
        ORDER BY TRADE_DATE ASC
    """

    result: queryResult = queryResult()

    with getConnection() as connection:
        with connection.cursor() as cursor:
            resultSet = cursor.execute(SQL,(buyerCurrencyID,exchangeID,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                result.B.append(row[1])
                result.C.append(row[2])
                #print(row)

    return result


def testQueryFour():

    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 1, 1, 0, 0, 0, 0)
    end = datetime(2018, 1, 14, 0, 0, 0, 0)
    myresult = queryFour(BTC,GEMINI,start, end)
    print(myresult)

if __name__ == "__main__":
    #testQueryFour()
    testConnection()