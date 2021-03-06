from datetime import datetime
import cx_Oracle
import os 
import sys 
from decouple import config
from re import search
import time

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

    def __init__(self):
        self.A = []
        self.B = []
        self.C = []


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

    DEBUG = config('DEBUG', default=False, cast=bool)
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
            cursor.prefetchrows = 10000
            cursor.arraysize = 10000
            resultSet = cursor.execute(SQL,(buyerCurrencyID,exchangeID,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                result.B.append(row[1])
                result.C.append(row[2])
                #print(row)

            cursorRowCount=cursor.rowcount
    if DEBUG:
        print("### buyerCurrencyID: {} exchangeID: {} startDate: {} endDate: {} RowCount: {} CursorRowCount: {} ".format(buyerCurrencyID,exchangeID,startDate,endDate,len(result.A),cursorRowCount ))
    return result


def testQueryOne():

    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 1, 1, 0, 0, 0, 0)
    end = datetime(2018, 1, 14, 0, 0, 0, 0)
    myresult = queryOne(BTC,GEMINI,start, end)


def queryTwo(exchangeID: int, startDate: datetime, endDate: datetime, ethCount: float, btcCount: float) -> queryResult:
    DEBUG = config('DEBUG', default=False, cast=bool)
    SQL = """
        WITH
        btcprice (TRADE_DATE, Bitcoin_Price) AS
        (SELECT TRADE_DATE,OPEN AS Bitcoin_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 1 AND EXCHANGE_ID = :1
        ORDER BY TRADE_DATE ASC),
        ethprice (TRADE_DATE, Ethereum_Price) AS
        (SELECT TRADE_DATE,OPEN AS Ethereum_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 2 AND EXCHANGE_ID = :2
        ORDER BY TRADE_DATE ASC)
        SELECT btcprice.trade_date, Ethereum_Price  ,Bitcoin_Price , Ethereum_Price * :3 ,Bitcoin_Price * :4
        FROM btcprice,ethprice
        WHERE btcprice.trade_date = ethprice.trade_date
        AND btcprice.trade_date between :5 and :6
        ORDER BY 1 ASC
    """

    result: queryResult = queryResult()

    with getConnection() as connection:
        with connection.cursor() as cursor:
            cursor.prefetchrows = 10000
            cursor.arraysize = 10000
            resultSet = cursor.execute(SQL,(exchangeID,exchangeID,ethCount,btcCount,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                result.B.append(row[3])
                result.C.append(row[4])

            cursorRowCount=cursor.rowcount
    if DEBUG:
        print("### exchangeID: {} startDate: {} endDate: {} RowCount: {} CursorRowCount: {} ".format(exchangeID,startDate,endDate,len(result.A),cursorRowCount ))

    return result

def testQueryTwo():
    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 2, 16, 0, 0, 0, 0)
    end = datetime(2018, 2, 17, 0, 0, 0, 0)
    myresult = queryTwo(GEMINI,start, end,8.5,20.0)
    print(myresult)

def queryThree(buyerCurrencyID:int, exchangeID: int, startDate: datetime, endDate: datetime) -> queryResult:
    DEBUG = config('DEBUG', default=False, cast=bool)
    SQL = """
        WITH
        btcprice_bitstamp (TRADE_DATE, Bitcoin_Price) AS
        (SELECT TRADE_DATE,OPEN AS Bitcoin_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 1 AND EXCHANGE_ID = :1
        ORDER BY TRADE_DATE ASC),
        ethprice_bitstamp (TRADE_DATE, Ethereum_Price) AS
        (SELECT TRADE_DATE,OPEN AS Ethereum_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 2 AND EXCHANGE_ID = :2
        ORDER BY TRADE_DATE ASC)
        SELECT btcprice_bitstamp.trade_date,Bitcoin_Price,Ethereum_Price,(Bitcoin_Price + Ethereum_Price)/2 AS Market_Price
        FROM btcprice_bitstamp,ethprice_bitstamp
        WHERE btcprice_bitstamp.trade_date = ethprice_bitstamp.trade_date
        AND btcprice_bitstamp.trade_date between :3 and :4 
        ORDER BY trade_date ASC
    """

    result: queryResult = queryResult()

    with getConnection() as connection:
        with connection.cursor() as cursor:
            cursor.prefetchrows = 10000
            cursor.arraysize = 10000
            resultSet = cursor.execute(SQL,(buyerCurrencyID,exchangeID,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                if buyerCurrencyID == 1: #Return Bitcoin_Price if buyerCurrencyID==1 (BTC)
                    result.B.append(row[1])
                else: # Return Ethereum_Price if buyerCurrencyID==2 (ETH)
                    result.B.append(row[2])
                
                result.C.append(row[3])
                #print(row)

            cursorRowCount=cursor.rowcount
    if DEBUG:
        print("### buyerCurrencyID: {} exchangeID: {} startDate: {} endDate: {} RowCount: {} CursorRowCount: {} ".format(buyerCurrencyID,exchangeID,startDate,endDate,len(result.A),cursorRowCount ))
    return result


def testQueryThree():

    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 1, 1, 0, 0, 0, 0)
    end = datetime(2018, 1, 14, 0, 0, 0, 0)
    myresult = queryThree(ETH,GEMINI,start, end)
    print(myresult)

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
            cursor.prefetchrows = 10000
            cursor.arraysize = 10000
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

def queryFive(exchangeID: int, startDate: datetime, endDate: datetime) -> queryResult:
    DEBUG = config('DEBUG', default=False, cast=bool)
    SQL = """
        WITH
        btcprice (TRADE_DATE, Bitcoin_Price) AS
        (SELECT TRADE_DATE,OPEN AS Bitcoin_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 1 AND EXCHANGE_ID = :1
        ORDER BY TRADE_DATE ASC),
        ethprice (TRADE_DATE, Ethereum_Price) AS
        (SELECT TRADE_DATE,OPEN AS Ethereum_Price
        FROM  KEREKOVSKIK.OHLC_DATA_POINT
        WHERE BUYER_CURRENCY = 2 AND EXCHANGE_ID = :2
        ORDER BY TRADE_DATE ASC)
        SELECT btcprice.trade_date, Ethereum_Price,Bitcoin_Price
        FROM btcprice,ethprice
        WHERE btcprice.trade_date = ethprice.trade_date
        AND btcprice.trade_date between :3 and :4
        ORDER BY 1 ASC
    """

    result: queryResult = queryResult()

    with getConnection() as connection:
        with connection.cursor() as cursor:
            cursor.prefetchrows = 10000
            cursor.arraysize = 10000
            resultSet = cursor.execute(SQL,(exchangeID,exchangeID,startDate,endDate))
            for row in resultSet:
                result.A.append(row[0])
                result.B.append(row[1])
                result.C.append(row[2])

            cursorRowCount=cursor.rowcount
    if DEBUG:
        print("### exchangeID: {} startDate: {} endDate: {} RowCount: {} CursorRowCount: {} ".format(exchangeID,startDate,endDate,len(result.A),cursorRowCount ))

    return result

def testQueryFive():

    # datetime(year, month, day, hour, minute, second, microsecond)
    start = datetime(2018, 2, 16, 0, 0, 0, 0)
    end = datetime(2018, 2, 17, 0, 0, 0, 0)
    myresult = queryFive(GEMINI,start,end)
    print(myresult)

def benchmarkQueries(start: datetime, end: datetime):

    
    print("Start: {}".format(start))
    print("End: {}".format(end))
    before = time.perf_counter_ns()
    myresult = queryOne(BTC,GEMINI,start, end)
    after = time.perf_counter_ns()
    duration = (after - before)/1000000
    print("Query One Time: {} ms".format(duration))

    before = time.perf_counter_ns()
    myresult = queryTwo(GEMINI,start, end,8.5,20.0)
    after = time.perf_counter_ns()
    duration = (after - before)/1000000
    print("Query Two Time: {} ms".format(duration))

    before = time.perf_counter_ns()
    myresult = queryThree(ETH,GEMINI,start, end)
    after = time.perf_counter_ns()
    duration = (after - before)/1000000
    print("Query Three Time: {} ms".format(duration))

    before = time.perf_counter_ns()
    myresult = queryFour(BTC,GEMINI,start, end)
    after = time.perf_counter_ns()
    duration = (after - before)/1000000
    print("Query Four Time: {} ms".format(duration))

    before = time.perf_counter_ns()
    myresult = queryFive(GEMINI,start,end)
    after = time.perf_counter_ns()
    duration = (after - before)/1000000
    print("Query Five Time: {} ms".format(duration))


def perfTest1D():
    start = datetime(2018, 2, 16, 0, 0, 0, 0)
    end = datetime(2018, 2, 17, 0, 0, 0, 0)
    benchmarkQueries(start,end)

def perfTest1M():
    start = datetime(2018, 2, 16, 0, 0, 0, 0)
    end = datetime(2018, 3, 16, 0, 0, 0, 0)
    benchmarkQueries(start,end)

def getTotalTupleCount() -> int:

    SQL = """
    select 
    (select  count(*) from kerekovskik.ohlc_data_point) +
    (select  count(*) from kerekovskik.currency) + 
    (select  count(*) from kerekovskik.exchange) as total
    from dual
    """

    total : int = 0
    with getConnection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            row = cursor.fetchone()
            total = row[0]

    return total

if __name__ == "__main__":
    #getTotalTupleCount()
    #testQueryTwo()
    #testQueryFour()
    #testQueryThree()
    #testQueryFive()
    testConnection()