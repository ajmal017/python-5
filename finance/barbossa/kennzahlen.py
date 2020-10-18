import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


df = pd.read_csv('peer_groups.csv', delimiter=';')
df = df.iloc[123:]

def create_api(ticker):
    return('https://eodhistoricaldata.com/api/fundamentals/{}?api_token=5ef9e1d3d885e2.21351768'.format(ticker))


for idx, row in tqdm(df.iterrows()):
    try:
        response = requests.get(create_api(row['stock_ticker']))
        data = response.json()


        """
        HIGHLIGHTS
        """

        highlights = pd.DataFrame(data['Highlights'], index=[0])
        highlights.fillna(0, inplace=True)
        highlights.columns

        h_values = []
        h_values.append(data['General']['Name'])
        h_values.append(data['General']['Code'])
        h_values.append(data['General']['Exchange'])
        h_values.append(data['General']['CurrencyCode'])

        print('{} Data received!'.format(data['General']['Name']))

        for col in highlights.columns:
            h_values.append(highlights[col].values[0])

        try:
            conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
            cur = conn.cursor()

            cur.execute(
                sql.SQL("insert into highlights values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                        %s, %s, %s, %s, %s, %s, %s, %s, %s)"), h_values)

            conn.commit()
            print('{} DONE!'.format(data['General']['Name']))

        except(Exception, psycopg2.DatabaseError) as error:
            print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
            print(error)

        """
        VALUATION
        """

        valuation = pd.DataFrame(data['Valuation'], index=[0])
        valuation.fillna(0, inplace=True)
        valuation.columns

        v_values = []
        v_values.append(data['General']['Name'])
        v_values.append(data['General']['Code'])
        v_values.append(data['General']['Exchange'])
        v_values.append(data['General']['CurrencyCode'])

        for col in valuation.columns:
            v_values.append(valuation[col].values[0])

        try:
            conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
            cur = conn.cursor()

            cur.execute(
                sql.SQL("insert into valuation values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"), v_values)

            conn.commit()
            print('{} DONE!'.format(data['General']['Name']))

        except(Exception, psycopg2.DatabaseError) as error:
            print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
            print(error)

        """
        SHARESSTATS
        """

        sharesstats = pd.DataFrame(data['SharesStats'], index=[0])
        sharesstats.fillna(0, inplace=True)
        sharesstats.columns

        ss_values = []
        ss_values.append(data['General']['Name'])
        ss_values.append(data['General']['Code'])
        ss_values.append(data['General']['Exchange'])
        ss_values.append(data['General']['CurrencyCode'])

        for col in sharesstats.columns:
            ss_values.append(sharesstats[col].values[0])

        print(ss_values)

        try:
            conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
            cur = conn.cursor()

            cur.execute(
                sql.SQL("insert into sharesstats values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s)"), ss_values)

            conn.commit()
            print('{} DONE!'.format(data['General']['Name']))

        except(Exception, psycopg2.DatabaseError) as error:
            print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
            print(error)

        """
        TECHNICALS
        """

        technicals = pd.DataFrame(data['Technicals'], index=[0])
        technicals.fillna(0, inplace=True)
        technicals.columns

        t_values = []
        t_values.append(data['General']['Name'])
        t_values.append(data['General']['Code'])
        t_values.append(data['General']['Exchange'])
        t_values.append(data['General']['CurrencyCode'])

        for col in technicals.columns:
            t_values.append(technicals[col].values[0])

        try:
            conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
            cur = conn.cursor()

            cur.execute(
                sql.SQL("insert into technicals values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s)"), t_values)

            conn.commit()
            print('{} DONE!'.format(data['General']['Name']))

        except(Exception, psycopg2.DatabaseError) as error:
            print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
            print(error)

        """
        BALANCE SHEET QUATERLY
        """

        bs_q = pd.DataFrame(data['Financials']['Balance_Sheet']['quarterly']).T
        bs_q.fillna(0, inplace=True)

        print(data['General']['Name'])

        for idx, row in bs_q.iterrows():

            bsq_values = []
            bsq_values.append(data['General']['Name'])
            bsq_values.append(data['General']['Code'])
            bsq_values.append(data['General']['Exchange'])
            bsq_values.append(data['General']['CurrencyCode'])

            for item in row.values:
                bsq_values.append(item)

            try:
                conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
                cur = conn.cursor()

                cur.execute(
                    sql.SQL("insert into balancesheetquarterly values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s)"), bsq_values)

                conn.commit()
                print('{} DONE!'.format(data['General']['Name']))

            except(Exception, psycopg2.DatabaseError) as error:
                print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
                print(error)
        #
        """
        CASH FLOW QUATERLY
        """

        cs_q = pd.DataFrame(data['Financials']['Cash_Flow']['quarterly']).T
        cs_q.fillna(0, inplace=True)

        print(data['General']['Name'])

        for idx, row in cs_q.iterrows():

            cfq_values = []
            cfq_values.append(data['General']['Name'])
            cfq_values.append(data['General']['Code'])
            cfq_values.append(data['General']['Exchange'])
            cfq_values.append(data['General']['CurrencyCode'])

            for item in row.values:
                cfq_values.append(item)

            try:
                conn = psycopg2.connect(host="95.217.128.174", database="barbossa", user="maximus", password="maximus")
                cur = conn.cursor()

                cur.execute(
                    sql.SQL("insert into cashflowquarterly values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                                                            %s, %s, %s, %s, %s, %s, %s, %s, %s)"), cfq_values)

                conn.commit()
                print('{} DONE!'.format(data['General']['Name']))

            except(Exception, psycopg2.DatabaseError) as error:
                print('{} Datenabfrage fehlgeschlagen'.format(data['General']['Name']))
                print(error)


        """
        INCOME STATEMENT QUATERLY
        """

        is_q = pd.DataFrame(data['Financials']['Income_Statement']['quarterly']).T
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
                    sql.SQL("insert into incomestatementquarterly values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
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
