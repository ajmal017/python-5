options = [
    {'label': 'ADIDAS', 'value': 'adidas'},
    {'label': 'Allianz', 'value': 'allianz'},
    {'label': 'BASF', 'value': 'basf'},
    {'label': 'Bayer', 'value': 'bayer'},
    {'label': 'Beiersdorf', 'value': 'beiersdorf'},
    {'label': 'BMW', 'value': 'bmw'},
    {'label': 'Continental', 'value': 'continental'},
    {'label': 'Covestro', 'value': 'covestro'},
    {'label': 'Daimler', 'value': 'daimler'},
    {'label': 'Deutsche Bank', 'value': 'deutschebank'},
    {'label': 'Deutsche Börse', 'value': 'deutscheboerse'},
    {'label': 'Deutsche Post', 'value': 'deutschepost'},
    {'label': 'Deutsche Telekom', 'value': 'telekom'},
    {'label': 'E.ON', 'value': 'eon'},
    {'label': 'Fresenius', 'value': 'Fresenius'},
    {'label': 'Fresenius Medical Care', 'value': 'freseniusmedical'},
    {'label': 'HeidelbergerCement', 'value': 'heidelbergercement'},
    {'label': 'Henkel', 'value': 'henkel'},
    {'label': 'Infineon', 'value': 'infineon'},
    {'label': 'Linde', 'value': 'linde'},
    {'label': 'Lufthansa', 'value': 'lufthansa'},
    {'label': 'Merck', 'value': 'merck'},
    {'label': 'MTU Aero Engines', 'value': 'mtu'},
    {'label': 'Münchener Rückversicherungs-Gesellschaft', 'value': 'muerueck'},
    {'label': 'SAP', 'value': 'sap'},
    {'label': 'Siemens', 'value': 'siemens'},
    {'label': 'Volkswagen', 'value': 'vw'},
    {'label': 'Vonovia', 'value': 'vonovia'},
    {'label': 'Wirecard', 'value': 'wirecard'}
]

for idx, option in enumerate(options):
    if option['value'] == 'adidas':
        company_name = option['label']
        print(company_name)

import psycopg2
from psycopg2 import sql
import pandas as pd
import plotly.express as px

conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")

cur = conn.cursor()
cur.execute(sql.SQL("""
            select branche_detail, branche_aggregiert from kennzahlen 
            where unternehmen = %s
        """), [company_name])
entries = cur.fetchall()
peers = pd.DataFrame(entries, columns=['branche_detail', 'branche_aggregiert'])


cur = conn.cursor()
cur.execute(sql.SQL("""
                    select * from kennzahlen 
                    where branche_detail = %s 
                    and branche_aggregiert = %s
                """), [peers['branche_detail'][0], peers['branche_aggregiert'][0]])
entries = cur.fetchall()
key_figures_peer = pd.DataFrame(entries,
                           columns=['unternehmen', 'branche_detail', 'branche_aggregiert', 'kennzahlen_link',
                                    'marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
                                    'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
                                    'cashflow_aktie', 'emissionspreis'])

key_figures_peer[['marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
    'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
    'cashflow_aktie', 'emissionspreis']] = key_figures_peer[['marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
    'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
    'cashflow_aktie', 'emissionspreis']].apply(pd.to_numeric)

print(key_figures_peer.info())

fig = px.scatter_ternary(key_figures_peer, a="anzahl_aktien", b="aktien_gewinn", c="buchwert_aktie",
                         color="unternehmen", size="marktkapitalisierung", size_max=50)
fig.show()

peer_companies = []
for peer in key_figures_peer['unternehmen']:
    peer_companies.append({'label':peer})

print(peer_companies)

# print(key_figures_peer)
# print(key_figures_peer.columns)