import requests
import pandas as pd
from bs4 import BeautifulSoup
import alpha_vantage
import pandas as pd
import requests
import psycopg2
from psycopg2 import sql
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

def crawl_stock(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"html.parser")

    tables = soup.findAll("table")

    for i in range(0, len(tables)):
        table = tables[i]
        if table.findParent("table") is None:
            t = pd.read_html(str(table))
            # print(t[0].shape)
            if t[0].shape == (7, 4):
                return t[0]

df = pd.read_csv('peer_groups.csv', delimiter=';')
df.columns = ['Unternehmen', 'branche_detail', 'branche_aggregiert', 'link']

for index, row in df.iterrows():
    stock = crawl_stock(row['link'])
    if stock is not  None:
        kennzahlen = stock.copy()
        # print(kennzahlen)
        val_1 = []
        val_2 = []
        for val in kennzahlen[1].values:
            try:
                temp = float(val) / 100
                if temp == None:
                    temp = 0
                val_1.append(temp)
            except:
                val_1.append(0)

        for val in kennzahlen[3].values:
            try:
                val_2.append(float(val) / 100)
            except:
                val_2.append(0)

        # val_1 = kennzahlen[1].values / 100
        kennzahlen[1] = val_1
        # val_2 = kennzahlen[3].values / 100
        kennzahlen[3] = val_2

        try:
            conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")
            cur = conn.cursor()

            # for index, row in df.iterrows():
            cur.execute(
                sql.SQL("insert into kennzahlen values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                                                            [row['Unternehmen'], \
                                                                             row['branche_detail'], \
                                                                             row['branche_aggregiert'], \
                                                                             row['link'], \
                                                                             float(kennzahlen[1][0]), \
                                                                             float(kennzahlen[1][1]), \
                                                                             float(kennzahlen[1][2]), \
                                                                             float(kennzahlen[1][3]), \
                                                                             float(kennzahlen[1][4]), \
                                                                             float(kennzahlen[3][0]), \
                                                                             float(kennzahlen[3][1]), \
                                                                             float(kennzahlen[3][2]), \
                                                                             float(kennzahlen[3][3]), \
                                                                             float(kennzahlen[3][4])])

            conn.commit()
            print('{} DONE!'.format(row['Unternehmen']))

        except(Exception, psycopg2.DatabaseError) as error:
                print('{} Schreiben der Daten fehlgeschlagen'.format(row['Unternehmen']))
                print(error)

    else:
        print('{} SKIPPED'.format(row['Unternehmen']))

    # def guv_stock(url):
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.text, "html.parser")
    #
    #     tables = soup.findAll("table")
    #
    #     guv = pd.DataFrame(columns=['chart', 'kennwert', '2013', '2014', '2015', '2016', '2017', '2018', '2019'])
    #
    #     # for i in range(1, len(tables)):
    #     #     table = tables[i]
    #     #     if table.findParent("table") is None:
    #     #         t = pd.read_html(str(table))
    #     #         # print(t[0].shape)
    #     #         if t[0].shape == (7, 4):
    #     #             return t[0]
    #
    #     table = tables[-1]
    #     if table.findParent("table") is None:
    #         t = pd.read_html(str(table))
    #         print(t[0].head())
    #         print(t[0].values)
    #         # guv = guv.append(t[0])
    #         # print(guv)


    # short = link.split('-')[0]
    # stock_name = short.split('/')[-1]
    #
    # guv_link = 'https://www.finanzen.net/bilanz_guv/{}'.format(stock_name)
    # print(guv_link)
    # print(kennezahlen)
    #
    # guv_stock(guv_link)
