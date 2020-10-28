
# visit http://127.0.0.1:8050/ in your web browser.
#Gráfico da quantidade de pessoas envolvidas nos acidentes em determinada situação clínica por estado (podendo variar o ano e a condição (ferido, morto, ileso...));
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

# Carrega a base de dados
df = pd.read_csv('dados_por_ocorrencia.csv', encoding='ISO-8859-1')

#Função para tirar dia e mês e deixar só o ano respectivo do dataframe
def replaceYear(df):
  if type(df) is str:
    date = df[:4]
    return int(date)
  else:
    return df

df['data_inversa'] = df['data_inversa'].apply(replaceYear)

# Carrega o css do html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Preparando o html com um dropdown dos tipos de estados clínicos e um slider para a variação dos anos
app.layout = html.Div([
    html.H1(
        children='Estado Clínico',
        style={
            'textAlign': 'center',
            'color': 'black'
        }
    ),

    html.Div(children='Estado Clínico das Vítimas por UF', style={
        'textAlign': 'center',
        'color': 'black'
    }),

    html.Div([
            html.Label('Estado_Clínico'),
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': 'Mortos', 'value': 'mortos'},
                    {
                        'label': 'Feridos Graves', 'value': 'feridos_graves'
                    },
                    {
                        'label': 'Feridos Leves', 'value': 'feridos_leves'
                    },
                    {
                        'label': 'Ilesos', 'value': 'ilesos'
                    }],
                    value='mortos'
                )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['data_inversa'].min(),
        max=df['data_inversa'].max(),
        value=df['data_inversa'].max(),
        marks={str(year): str(year) for year in df['data_inversa'].unique()},
        step=None
    )
])

#Faz com que atualize automaticamente após as mudanças
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column,year_value):
    dff = df[df['data_inversa'] == year_value]
    #Agrupando a quantidade de pessoas por cada estado
    dados_por_ocorrencia2 = dff.groupby(['uf']).sum()

    #Gráfico de colunas
    fig = px.bar(dados_por_ocorrencia2,x=dados_por_ocorrencia2.index,y=xaxis_column)

    fig.update_layout(transition_duration=500)
    return fig


# Sobe o servidor e realiza a recarga automática da página
if __name__ == '__main__':
    app.run_server(debug=True)