# To set up Instant Client 

```bash
for x in `ls oracle_libs/*`; do unzip ${x}; done
```

# Create Virtual Environment

```bash
python3 -m venv venv 
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
# Download data

Downloade from https://www.cryptodatadownload.com/ 

# Prepare the data 

```bash
tar -xf data.tar.gz
for x in `ls data/*.csv`; do sed -i '1d' ${x}; done
```

# Load the data 

```bash
python3 import_data.py data/Bitstamp_BTCUSD_2018_minute.csv bitstamp btc
python3 import_data.py data/Bitstamp_BTCUSD_2019_minute.csv bitstamp btc
python3 import_data.py data/Bitstamp_BTCUSD_2020_minute.csv bitstamp btc
python3 import_data.py data/Bitstamp_BTCUSD_2021_minute.csv bitstamp btc

python3 import_data.py data/Bitstamp_ETHUSD_2018_minute.csv bitstamp eth
python3 import_data.py data/Bitstamp_ETHUSD_2019_minute.csv bitstamp eth
python3 import_data.py data/Bitstamp_ETHUSD_2020_minute.csv bitstamp eth
python3 import_data.py data/Bitstamp_ETHUSD_2021_minute.csv bitstamp eth

python3 import_data.py data/gemini_BTCUSD_2018_1min.csv gemini btc 
python3 import_data.py data/gemini_BTCUSD_2019_1min.csv gemini btc
python3 import_data.py data/gemini_BTCUSD_2020_1min.csv gemini btc
python3 import_data.py data/Gemini_BTCUSD_2021_1min.csv gemini btc 


python3 import_data.py data/gemini_ETHUSD_2018_1min.csv gemini eth
python3 import_data.py data/gemini_ETHUSD_2019_1min.csv gemini eth
python3 import_data.py data/gemini_ETHUSD_2020_1min.csv gemini eth
python3 import_data.py data/Gemini_ETHUSD_2021_1min.csv gemini eth

```
