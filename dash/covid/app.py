import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

covid19 = pd.read_csv('covid19.csv', index_col='Date')
covid19.index = pd.to_datetime(covid19.index)
covid19_country = pd.read_csv('covid_per_country.csv', index_col=[0])

today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)

last_week = covid19.loc[week_ago:today]


worldmap = px.scatter_geo(last_week, locations='alpha3', color="Deaths",hover_name="Country",size="Confirmed",
                            projection="orthographic")

app.layout = html.Div(children=[
    html.H1(children='COVID-19 Interactive Dashboard'),

    # Div for first graph
    html.Div([
        html.H2(children='World overview'),
        dcc.Graph(
            id='world-overview',
            figure= worldmap
        )
    ]),

    html.H2(children='Select the continent you are interested in:'),

    # Second Plot
    html.Div([
        html.Div([
                dcc.Dropdown(
                    id='continent-select',
                    options=[
                            {'label': 'Europe', 'value': 'Europe'},
                            {'label': 'Asia', 'value': 'Asia'},
                            {'label': 'Americas', 'value': 'Americas'},
                            {'label': 'Oceania', 'value': 'Oceania'}
                        ],
                    value=['Europe'],
                    multi=True
                )
            ],
            style={'width': '50%',  'verticalAlign': 'middle'}),

        html.Div([
            dcc.Graph(
                id='continent-overview',
                figure= {}
        )
        ],
        style={'width': '100%'})
    ])

])

@app.callback(
    dash.dependencies.Output('continent-overview', 'figure'),
    [dash.dependencies.Input('continent-select', 'value')]
)
def update_continent(cont):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    last_week = covid19.loc[week_ago:today]

    print(len(cont))

    if len(cont) == 1:
        continent = last_week[last_week['continent'] == cont[0]]
        fig = px.scatter(continent, x='Confirmed', y='Deaths', hover_name='Country', log_y=True, color='Country')
        return fig

    elif len(cont) == 2:
        continent = last_week[(last_week['continent'] == cont[0]) | (last_week['continent'] == cont[1])]
        fig = px.scatter(continent, x='Confirmed', y='Deaths', hover_name='Country', log_y=True, color='Country')
        return fig

    elif len(cont) == 3:
        continent = last_week[(last_week['continent'] == cont[0]) | (last_week['continent'] == cont[1])| (last_week['continent'] == cont[2])]
        fig = px.scatter(continent, x='Confirmed', y='Deaths', hover_name='Country', log_y=True, color='Country')
        return fig

    elif len(cont) == 4:
        continent = last_week[(last_week['continent'] == cont[0]) | (last_week['continent'] == cont[1]) | (last_week['continent'] == cont[2]) | (last_week['continent'] == cont[3])]
        fig = px.scatter(continent, x='Confirmed', y='Deaths', hover_name='Country', log_y=True, color='Country')
        return fig

if __name__ == '__main__':
    app.run_server(debug=True)
