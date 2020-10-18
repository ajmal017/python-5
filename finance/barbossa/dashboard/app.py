import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import  plotly.graph_objects as go
import datetime
from datetime import date
import psycopg2
from psycopg2 import sql
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

app.layout = html.Div(children=[
    html.H1(children='DAX Aktienanalyse Tool'),
    html.Div(children='''
        DAX - Aktie auswählen und Betrachtungszeitraum angeben
    '''),
    html.Div(),
    html.Div(children=[
        html.Div(children=[
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=datetime.datetime(2000, 1, 1),
                max_date_allowed=date.today(),
                start_date= datetime.datetime.now() - datetime.timedelta(30),
                end_date=date.today(),
                calendar_orientation='vertical',
                style=dict(
                    verticalAlign="top",
                    width='100%'
                )
            )
        ], style={'width': '50%', 'display':'inline-block'}),
        html.Div(children=[
            dcc.Dropdown(
                id='stock-dropdown',
                options=options,
                value='adidas',
                style=dict(
                    verticalAlign="top",
                    width='100%'
                )
            )
        ], style={'width': '50%', 'display':'inline-block'})
    ], style={'width': '100%', 'display':'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='candle-chart')
    ], style={'width': '100%', 'display':'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='traded-volume')
    ], style={'width': '100%', 'display':'inline-block'}),
    html.Div(),
    html.H1('Kennzahlen und Peer-Gruppe'),
    html.Div(children='Peer Gruppe:'),
    html.Div(children=[
        dcc.RadioItems(id='peer-group', labelStyle={'display': 'inline-block'})
    ], style={'width': '100%', 'display':'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='kgvs')
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='aktien')
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div(children=[
        dcc.Graph(id='cashflow')
    ], style={'width': '100%', 'display': 'inline-block'})

])

@app.callback([Output('candle-chart', 'figure'),
              Output('traded-volume', 'figure'),
               Output('kgvs', 'figure'),
               Output('peer-group', 'options'),
               Output('aktien', 'figure'),
               Output('cashflow', 'figure')],
              [Input('date-picker', 'start_date'),
               Input('date-picker', 'end_date'),
               Input('stock-dropdown', 'value')])
def update_candle(start, end, name):
    try:
        conn = psycopg2.connect(host="95.217.128.174", database="maximus", user="maximus", password="maximus")
        cur = conn.cursor()
        cur.execute(sql.SQL("""
            select * from dax where
            date >= %s and date <= %s and name = %s
            ORDER BY date ASC
        """),[start, end, name])
        records = cur.fetchall()
        df = pd.DataFrame(records, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'name'])

        candle = go.Figure(data=[go.Candlestick(x=df['date'],
                                             open=df['open'],
                                             high=df['high'],
                                             low=df['low'],
                                             close=df['close'])])
        candle.update_layout(
            title="Kursverlauf",
            xaxis_title="Datum",
            yaxis_title="Aktienkurs",
            height=800)

        volume = px.line(df, x='date', y='volume', title='Gehandeltes Volumen', labels={'date':'Datum', 'volume':'Gehanldetes Volumen'})

        for idx, option in enumerate(options):
            if option['value'] == name:
                company_name = option['label']

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
                                        columns=['unternehmen', 'branche_detail', 'branche_aggregiert',
                                                 'kennzahlen_link',
                                                 'marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
                                                 'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
                                                 'cashflow_aktie', 'emissionspreis'])

        key_figures_peer[['marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
                          'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
                          'cashflow_aktie', 'emissionspreis']] = key_figures_peer[
            ['marktkapitalisierung', 'streubesitz', 'kbv', 'kcv', 'kgv',
             'anzahl_aktien', 'aktien_gewinn', 'buchwert_aktie',
             'cashflow_aktie', 'emissionspreis']].apply(pd.to_numeric)

        peer_companies = []
        for peer in key_figures_peer['unternehmen']:
            peer_companies.append({'label':peer})

        kgvs = px.scatter(key_figures_peer, x="kbv", y="kcv", size="kgv", color="unternehmen", size_max=120, title='KBV - KCV - KGV Verhältniss',
                                            labels={'kbv':'KBV', 'kcv':'KCV', 'kgv':'KGV'})

        aktien = px.scatter_ternary(key_figures_peer, a="anzahl_aktien", b="aktien_gewinn", c="buchwert_aktie",
                                                        color="unternehmen", size="marktkapitalisierung", size_max=50,
                                                        labels={'anzahl_aktien':'Aktienanzahl', 'aktien_gewinn':'Gewinn pro Aktie',
                                                                'buchwert_aktie':'Buchwert pro Aktie'})

        cashflow = px.bar(key_figures_peer, x='unternehmen', y='cashflow_aktie',
             hover_data=['kbv', 'kcv', 'kgv'], color='streubesitz', labels={'cashflow_aktie':'Cashflow pro Aktie', 'unternehmen':'Unternehmen'})

        return candle, volume, kgvs, peer_companies, aktien, cashflow

    except(Exception, psycopg2.DatabaseError) as error:
            print('{} Datenabfrage fehlgeschlagen'.format(name))
            print(error)

if __name__ == '__main__':
    app.run_server(debug=False)