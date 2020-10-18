import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

df = pd.read_csv('peer_groups.csv', delimiter=';')
# df = df.iloc[123:]


def create_api(ticker):
    return ('https://eodhistoricaldata.com/api/fundamentals/{}?api_token=5ef9e1d3d885e2.21351768'.format(ticker))


for idx, row in tqdm(df.iterrows()):
    try:
        response = requests.get(create_api(row['stock_ticker']))
        data = response.json()


        """
        INCOME STATEMENT YEARLY
        """

        is_q = pd.DataFrame(data['Financials']['Income_Statement']['yearly']).T
        is_q.fillna(0, inplace=True)

        print(data['General']['Name'])

        for idx, row in is_q.iterrows():

            isq_values = []
            isq_values.append(data['General']['Name'])
            isq_values.append(data['General']['Code'])
            isq_values.append(data['General']['Exchange'])
            isq_values.append(data['General']['CurrencyCode'])

            for item in row.values:
                isq_values.append(item)

            try:
                conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
                cur = conn.cursor()

                cur.execute(
                    sql.SQL("insert into incomestatementyearly values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                             %s, %s, %s, %s)"), isq_values)

                conn.commit()
                print('{} DONE!'.format(data['General']['Name']))

            except(Exception, psycopg2.DatabaseError) as error:
                print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
                print(error)


    except:
        print('error')
