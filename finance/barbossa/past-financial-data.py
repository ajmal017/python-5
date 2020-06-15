import pandas as pd
import quandl
import psycopg2
from psycopg2 import sql

dax_konzerne = {
    'adidas':'ADS_X',
    'allianz':'ALV_X',
    'basf':'BAS_X',
    'bayer':'BAYN_X',
    'beiersdorf':'BEI_X',
    'bmw':'BMW_X',
    'continental':'CON_X',
    'covestro':'',
    'daimler':'DAI_X',
    'deutschebank':'DKB_X',
    'deutschepost':'DPW_X',
    'telekom':'DTE_X',
    'deutscheboerse':'DB1_X',
    'eon':'EON_X',
    'fresenius':'FRE_X',
    'freseniusmedical':'FMW_X',
    'heidelbergercement':'',
    'henkel':'HEN3_X',
    'infineon':'IFX_X',
    'linde':'LIN_X',
    'lufthansa':'LHA_X',
    'merck':'MRK_X',
    'mtu':'MTX_X',
    'muerueck':'MUV2_X',
    'rwe':'RWE_X',
    'sap':'SAP_X',
    'siemens':'SIE_X',
    'vw':'VOW3_X',
    'vonovia':'',
    'wirecard':''
}

for key, value in dax_konzerne.items():
    if value != '':

        try:

            df = quandl.get("FSE/{}".format(value), authtoken="eSQL3KzSTGXurQhGkt8A", start_date="2018-01-01")
            df = df[['Open', 'High', 'Low', 'Close']]

        except:
            print('{} FAILED LOADING DATA FROM QUANDL'.format(key))

        # Write to db
        try:
            conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")
            cur = conn.cursor()

            # i = 0

            for index, row in df.iterrows():
                cur.execute(
                    sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s)").format(sql.Identifier(key)),
                                                                                [index, \
                                                                                row['Open'], \
                                                                                row['High'], \
                                                                                row['Low'], \
                                                                                row['Close'], \
                                                                                key])
                # i += 1

            conn.commit()

        except(Exception, psycopg2.DatabaseError) as error: \
            print(error)

    print('{} DONE!'.format(key))
    break



