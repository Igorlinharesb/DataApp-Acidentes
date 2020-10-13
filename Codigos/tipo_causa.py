# Run this app with `python tipo_causa.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Carrega a base de dados, coloque ela no caminho que desejar
path = 'dados_por_ocorrencia.csv'
df = pd.read_csv(path, encoding='ISO-8859-1')

# Carrega o css do html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Substituindo data_inversa pelo ano

def replaceYear(df):
  if type(df) is str:
    date = df[:4]
    return int(date)
  else:
    return df

df['data_inversa'] = df['data_inversa'].apply(replaceYear)

remove = df.loc[(df['causa_acidente'] == 'outras')]
df = df.drop(remove.index)

df = df.rename(columns={'id': 'Qtd de Acidentes', 'data_inversa': 'ano'})


# Prepara o html
app.layout = html.Div(children=[
    html.H1(
        children='Ocorrências',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ),

    html.Div(children='Ocorrências por tipo e causa de acidentes', style={
        'textAlign': 'center',
        'color': 'black'
    }),

    html.Div([
        html.Label('Tipo de Dado'),
        dcc.Dropdown(
            id='xaxis-column',
            options=[
                {'label': 'Tipo de Acidente', 'value': 'tipo_acidente'},
                {'label': 'Causa de Acidente', 'value': 'causa_acidente'}            
            ],
            value='tipo_acidente'
        )       
    ], style={'width': '48%'}),    

    dcc.Graph(
        id='graph-with-slider'        
    ),
    
    dcc.Slider(
        id='year-slider',
        min=df['ano'].min(),
        max=df['ano'].max(),
        value=df['ano'].min(),
        marks={str(year): str(year) for year in df['ano'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('xaxis-column', 'value')])
def update_figure(selected_year, xaxis_value):
    filtered_df = df[df.ano == selected_year]

    # Faz uma contagem da quantidade de acidentes por tipo de acidente
    new_df = filtered_df.set_index([xaxis_value, "uf"]).count(level=xaxis_value)    

    fig = px.bar(new_df, x=new_df.index, y="Qtd de Acidentes")

    fig.update_layout(transition_duration=500)

    return fig

# Sobe o servidor e realiza a recarga automática da página
if __name__ == '__main__':
    app.run_server(debug=True)