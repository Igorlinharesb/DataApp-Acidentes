
# visit http://127.0.0.1:8050/ in your web browser.
#Gráfico da quantidade de pessoas envolvidas nos acidentes em determinada situação clínica por estado (podendo variar o ano e a condição (ferido, morto, ileso...));
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

# Carrega a base de dados
dfano = pd.read_csv('pessoas_mes_ano.csv', encoding='ISO-8859-1')


months = {
          1: "Jan",
          2: "Fev",
          3: "Mar",
          4: "Abril",
          5: "Maio",
          6: "Jun",
          7: "Jul",
          8: "Ago",
          9: "Set",
          10: "Out",
          11: "Nov",
          12: "Dez",                        
            
                  }

dfano['mes'] = dfano['mes'].replace(months)



# Carrega o css do html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Preparando o html com um dropdown dos meses e um slider para a variação dos anos
app.layout = html.Div([
    html.Div([
            html.Label('Estado_Clínico'),
                dcc.Dropdown(
                    id='xaxiss-column',
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

    dcc.Graph(id='indicador-graphic'),

    dcc.Slider(
        id='ano--slider',
        min=dfano['ano'].min(),
        max=dfano['ano'].max(),
        value=dfano['ano'].max(),
        marks={str(year): str(year) for year in dfano['ano'].unique()},
        step=None
    )
])

#Faz com que atualize automaticamente após as mudanças
@app.callback(
    Output('indicador-graphic', 'figure'),
    [Input('xaxiss-column', 'value'),
     Input('ano--slider', 'value')])
def update_graph(xaxis_column,year_value):
    dff = dfano[dfano['ano'] == year_value]
  
    #Gráfico de colunas
    fig = px.bar(dff,x=dff['mes'],y=xaxis_column)

    fig.update_layout(transition_duration=500)
    return fig


# Sobe o servidor e realiza a recarga automática da página
if __name__ == '__main__':
    app.run_server(debug=True)