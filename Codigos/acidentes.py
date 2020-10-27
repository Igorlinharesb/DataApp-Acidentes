
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

#Criando as colunas de ano e mês
df['ano'] = df['data_inversa'].apply(lambda x: int(str(x)[:4]))
df['mes'] = df['data_inversa'].apply(lambda x: str(x)[5:7])
'''
months = {
          "1": "Jan",
          "2": "Fev",
          "3": "Mar",
          "4": "Abril",
          "5": "Maio",
          "6": "Jun",
          "7": "Jul",
          "8": "Ago",
          "9": "Set",
          "10": "Out",
          "11": "Nov",
          "12": "Dez",                        
            
                  }

df['mes'] = df['mes'].replace(months)'''



# Carrega o css do html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Preparando o html com um dropdown dos meses e um slider para a variação dos anos
app.layout = html.Div([
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
        min=df['ano'].min(),
        max=df['ano'].max(),
        value=df['ano'].max(),
        marks={str(year): str(year) for year in df['ano'].unique()},
        step=None
    )
])

#Faz com que atualize automaticamente após as mudanças
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column,year_value):
    dff = df[df['ano'] == year_value]
    #Agrupando a quantidade de pessoas por cada mês
    dados_por_ocorrencia2 = dff.groupby(['mes']).sum()

    #Gráfico de colunas
    fig = px.bar(dados_por_ocorrencia2,x=dados_por_ocorrencia2.index,y=xaxis_column)

    fig.update_layout(transition_duration=500)
    return fig


# Sobe o servidor e realiza a recarga automática da página
if __name__ == '__main__':
    app.run_server(debug=True)