alter session set nls_date_format=‘YYYY-MM-DD HH24:MI:SS’;
-- Query 1: Daily Percentage Change in Price for a Given Crypto
--BTC Percent Change,  Gemini
SELECT trade_date,open,
       - 100.0 * (1 - LEAD(open) OVER (ORDER BY trade_date) / open) AS Percent_Change
FROM KEREKOVSKIK.OHLC_DATA_POINT
WHERE buyer_currency =‘1’ AND exchange_id = ‘1’
ORDER BY trade_date ASC;
--BTC Percent Change,  Bitstamp
SELECT trade_date,open,
       - 100.0 * (1 - LEAD(open) OVER (ORDER BY trade_date) / open) AS Percent_Change
FROM KEREKOVSKIK.OHLC_DATA_POINT
WHERE buyer_currency =‘1’ AND exchange_id = ‘2’
ORDER BY trade_date ASC;
--ETH Percent Change,  Gemini
SELECT trade_date,open,
       - 100.0 * (1 - LEAD(open) OVER (ORDER BY trade_date) / open) AS Percent_Change
FROM KEREKOVSKIK.OHLC_DATA_POINT
WHERE buyer_currency =‘2’ AND exchange_id = ‘1’
ORDER BY trade_date ASC;
--ETH Percent Change,  Bitstamp
SELECT trade_date,open,
       - 100.0 * (1 - LEAD(open) OVER (ORDER BY trade_date) / open) AS Percent_Change
FROM KEREKOVSKIK.OHLC_DATA_POINT
WHERE buyer_currency =‘2’ AND exchange_id = ‘2’
ORDER BY trade_date ASC;
09:08
-- Query 4: Trading Volume Over Time for a given Crypto
--Bitcoin, Gemini
SELECT TRADE_DATE, BUYER_CURRENCY,VOLUME
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘1’ AND EXCHANGE_ID = ‘1’
ORDER BY TRADE_DATE ASC;
--Bitcoin, Bitstamp
SELECT TRADE_DATE, BUYER_CURRENCY,VOLUME
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘1’ AND EXCHANGE_ID = ‘2’
ORDER BY TRADE_DATE ASC;
--Ethereum, Gemini
SELECT TRADE_DATE, BUYER_CURRENCY,VOLUME
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘2’ AND EXCHANGE_ID = ‘1’
ORDER BY TRADE_DATE ASC;
--Ethereum, Bitstamp
SELECT TRADE_DATE, BUYER_CURRENCY,VOLUME
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘2’ AND EXCHANGE_ID = ‘2’
ORDER BY TRADE_DATE ASC;
-------------------------------------------------------------------------------
-- Query 5: Correlation Between Different Cryptos Over Time
--Bitcoin Price, Gemini
CREATE TABLE BTC_PRICE_GEMINI
AS
SELECT TRADE_DATE,OPEN AS Bitcoin_Price
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘1’ AND EXCHANGE_ID = ‘1’
ORDER BY TRADE_DATE ASC;
--Bitcoin Price, Bitstamp
CREATE TABLE BTC_PRICE_BITSTAMP
AS
SELECT TRADE_DATE,OPEN AS Bitcoin_Price
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘1’ AND EXCHANGE_ID = ‘2’
ORDER BY TRADE_DATE ASC;
--Ethereum Price, Gemini
CREATE TABLE ETH_PRICE_GEMINI
AS
SELECT TRADE_DATE,OPEN AS Ethereum_Price
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘2’ AND EXCHANGE_ID = ‘1’
ORDER BY TRADE_DATE ASC;
--Ethereum Price, Bitstamp
CREATE TABLE ETH_PRICE_BITSTAMP
AS
SELECT TRADE_DATE,OPEN AS Ethereum_Price
FROM  KEREKOVSKIK.OHLC_DATA_POINT
WHERE BUYER_CURRENCY = ‘2’ AND EXCHANGE_ID = ‘2’
ORDER BY TRADE_DATE ASC;
select * from btc_price_bitstamp;
--Gemini BTC-ETH CORRELATION - Creates Table w/ Side by Side Price - Line of best fit?
SELECT btc_price_gemini.trade_date, Ethereum_Price,Bitcoin_Price
FROM btc_price_gemini,eth_price_gemini
WHERE btc_price_gemini.trade_date = eth_price_gemini.trade_date
ORDER BY trade_date ASC;
--BITSTAMP BTC-ETH CORRELATION - Creates Table w/ Side by Side Price - Line of best fit?
SELECT btc_price_bitstamp.trade_date, Ethereum_Price,Bitcoin_Price
FROM btc_price_bitstamp,eth_price_bitstamp
WHERE btc_price_bitstamp.trade_date = eth_price_bitstamp.trade_date
ORDER BY trade_date ASC;