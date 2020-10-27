# Run this app with `python tipo_causa.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Carrega as bases de dados, coloque ela no caminho que desejar

df_causa_acidente = pd.read_csv('causa_acidente.csv', encoding='ISO-8859-1', sep=';')
df_tipo_acidente = pd.read_csv('tipo_acidente.csv', encoding='ISO-8859-1', sep=';')

# Carrega o css do html
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# def replaceYear(df):
#   if type(df) is str:
#     date = df[:4]
#     return int(date)
#   else:
#     return df

# df['data_inversa'] = df['data_inversa'].apply(replaceYear)

# remove = df.loc[(df['causa_acidente'] == 'outras')]
# df = df.drop(remove.index)

# df = df.rename(columns={'id': 'Qtd de Acidentes', 'data_inversa': 'ano'})


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
        min=df_causa_acidente['ano'].min(),
        max=df_causa_acidente['ano'].max(),
        value=df_causa_acidente['ano'].min(),
        marks={str(year): str(year) for year in df_causa_acidente['ano'].unique()},
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
    Input('xaxis-column', 'value')])
    
def update_figure(selected_year, xaxis_value):
    if xaxis_value == 'causa_acidente':
        filtered_causa_df = df_causa_acidente[df_causa_acidente.ano == selected_year]
        # Faz uma contagem da quantidade de acidentes por tipo de acidente        

        fig = px.bar(filtered_causa_df, x="causa_acidente", y="Qtd Acidentes")

        fig.update_layout(transition_duration=500)

        return fig
    elif xaxis_value == 'tipo_acidente':
        filtered_tipo_df = df_tipo_acidente[df_tipo_acidente.ano == selected_year]
        # Faz uma contagem da quantidade de acidentes por tipo de acidente        


        fig = px.bar(filtered_tipo_df, x="tipo_acidente", y="Qtd Acidentes")

        fig.update_layout(transition_duration=500)

        return fig

# Sobe o servidor e realiza a recarga automática da página
if __name__ == '__main__':
    app.run_server(debug=True)