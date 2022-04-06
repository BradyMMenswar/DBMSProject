import cx_Oracle
import os 
import sys 
from decouple import config
from re import search

def testConnection():

    # Get config info from .env file
    USER = config('myuser')
    PASSWORD = config('mypw')
    DSN = config('mydsn')


    #Modify the path variable to contain instant client DLLs
    if search("instantclient-basic-windows.x64-21.3.0.0.0", os.environ["PATH"]):
        print("Instant client in PATH, doing nothing")
    else:
        print("Instant client NOT found in PATH variable... Attempting to set it manually")
        currentPath= os.environ["PATH"]
        os.environ["PATH"] = "{};{}".format(".\instantclient-basic-windows.x64-21.3.0.0.0\instantclient_21_3",currentPath) 

    # Establish the database connection
    with cx_Oracle.connect(user=USER, password=PASSWORD,dsn=DSN) as connection:

        # Obtain a cursor
        cursor = connection.cursor()

        SQL = """
        select 'it works' from dual
        """

        rows = cursor.execute(SQL)
        for x in rows:
            print(x)

if __name__ == "__main__":
    testConnection()