import alpha_vantage
import pandas as pd
import requests
import psycopg2
from psycopg2 import sql

df = pd.DataFrame()
API_URL = "https://www.alphavantage.co/query"

dax_konzerne = {
    'adidas':'ADS',
    'allianz':'ALV',
    'basf':'BAS',
    'bayer':'BAYN',
    'beiersdorf':'BEI',
    'bmw':'BMW',
    'continental':'CON',
    'covestro':'1COV',
    'daimler':'DAI',
    'deutschebank':'DKB',
    'deutschepost':'DPW',
    'telekom':'DTE',
    'deutscheboerse':'DB1',
    'eon':'EON',
    'fresenius':'FRE',
    'freseniusmedical':'FMW',
    'heidelbergercement':'HEI',
    'henkel':'HEN3',
    'infineon':'IFX',
    'linde':'LIN',
    'lufthansa':'LHA',
    'merck':'MRK',
    'mtu':'MTX',
    'muerueck':'MUV2',
    'rwe':'RWE',
    'sap':'SAP',
    'siemens':'SIE',
    'vw':'VOW3',
    'vonovia':'VNA',
    'wirecard':'WDI'
}

prefix = '.DE'

for name, symbol in dax_konzerne.items():
    data = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol + '.DE',
        "outputsize": "full",
        "apikey": "OQ123LDEVEFUR30U",
        }
    try:
        response = requests.get(API_URL, params=data)
        data = response.json()
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.columns = ['open', 'high', 'low', 'close', 'adjusted_close',
           'volume', 'dividend_amount', 'split_coefficient']
        print(df)
        break
    except:
        print('{} Datenabfrage fehlgeschlagen'.format(name))

    # Write to db
    # try:
    #     conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")
    #     cur = conn.cursor()
    #
    #     for index, row in df.iterrows():
    #         cur.execute(
    #             sql.SQL("insert into dax values (%s, %s, %s, %s, %s, %s, %s)"), [index, \
    #                                                                          row['open'], \
    #                                                                          row['high'], \
    #                                                                          row['low'], \
    #                                                                          row['close'], \
    #                                                                          row['volume'], \
    #                                                                          name])
    #
    #     conn.commit()
    #     print('{} DONE!'.format(name))
    #
    # except(Exception, psycopg2.DatabaseError) as error:
    #         print('{} Datenabfrage fehlgeschlagen'.format(name))
    #         print(error)