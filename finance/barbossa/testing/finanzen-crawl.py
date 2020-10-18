import requests
import pandas as pd
from bs4 import BeautifulSoup
import alpha_vantage
import pandas as pd
import requests
import psycopg2
from psycopg2 import sql

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


df = crawl_stock("https://www.finanzen.net/aktien/activision_blizzard-aktie")

if not df.empty:
    print(df.head())

# df = pd.read_csv('peer_groups.csv', delimiter=';').drop('Unnamed: 4', axis=1)
# print(df.head())
# print(df.columns)
#
#
# # Write to db
#     try:
#         conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")
#         cur = conn.cursor()
#
#         # for index, row in df.iterrows():
#         cur.execute(
#             sql.SQL("insert into daily values (%s, %s, %s, %s, %s, %s, %s)"), [df.index[0], \
#                                                                          df['open'][0], \
#                                                                          df['high'][0], \
#                                                                          df['low'][0], \
#                                                                          df['close'][0], \
#                                                                          df['volume'][0], \
#                                                                          name])
#
#         conn.commit()
#         print('{} DONE!'.format(name))
#
#     except(Exception, psycopg2.DatabaseError) as error:
#             print('{} Datenabfrage fehlgeschlagen'.format(name))
#             print(error)