import json
from urllib.request import urlopen

import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Importando a base de dados
df = pd.read_csv('df_ano_uf.csv', encoding='ISO-8859-1')
df_pessoa = pd.read_csv('pessoas_uf_ano.csv', encoding='ISO-8859-1')

# Layout
app.layout = html.Div(
    [

        html.H1("TITULO DA PÁGINA", style={'text-align': 'center'}),

        dcc.Dropdown(
            id='tipo',
            options=[
                {"label": "Acidentes", "value": "acidentes"},
                {"label": "Mortos", "value": "mortos"},
                {"label": "Feridos", "value": "feridos"},
                {"label": "Ilesos", "value": "ilesos"},
                ],
            value="acidentes",
            style={'width': "30%"}),
        
        dcc.Dropdown(
            id='anos',
            options=[
                {"label": "2007", "value": 2007},
                {"label": "2008", "value": 2008},
                {"label": "2009", "value": 2009},
                {"label": "2010", "value": 2010},
                {"label": "2011", "value": 2011},
                {"label": "2012", "value": 2012},
                {"label": "2013", "value": 2013},
                {"label": "2014", "value": 2014},
                {"label": "2015", "value": 2015},
                {"label": "2016", "value": 2016},
                {"label": "2017", "value": 2017},
                {"label": "2018", "value": 2018},
                {"label": "2019", "value": 2019},
                {"label": "2020", "value": 2020}
            ],
            value=2020,
            style={'width': "30%"}),

        html.H4(id='message', children=[], style={'text-align': 'left'}),
        html.Br(),

        dcc.Graph(id='map-container', figure={}, style={'text-align': 'center'})
    ]
)

# Callbacks
@app.callback(
    [
        Output(component_id='message', component_property='children'),
        Output(component_id='map-container', component_property='figure'),
        Input(component_id='anos', component_property='value'),
        Input(component_id='tipo', component_property='value')
    ]
)
def update_map(ano, tipo):
    
    container = [f"Mapa com número de {tipo} em: {ano}"]

    # Arquivo geojson com o shape do Brasil
    url = 'https://raw.githubusercontent.com/samuelamico/Mapas_Brasil/master/Mapas/Estados.geojson'
    with urlopen(url) as response:
        br = json.load(response)

    
    if tipo == 'acidentes':
        # Filtrando os dados com base no intervalo de entrada
        df_ano_uf = df[df['ano'] == ano]

        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.acidentes,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'acidentes'],
                        width=700)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de acidentes",
                                                lenmode="pixels", len=200))


    df_ano_uf = df_pessoa[df_pessoa['ano'] == ano]

    if tipo == 'mortos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.mortos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'mortos'],
                        width=700)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de mortes",
                                                lenmode="pixels", len=200))
    if tipo == 'mortos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.mortos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'mortos'],
                        width=700)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de mortes",
                                                lenmode="pixels", len=200))


    if tipo == 'feridos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.feridos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'feridos'],
                        width=700)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de feridos",
                                                lenmode="pixels", len=200))
           
    if tipo == 'ilesos':
        # Gerando o gráfico com plotly express
        fig = px.choropleth(
                        df_ano_uf,
                        geojson=br,
                        color=df_ano_uf.ilesos,
                        color_continuous_scale='YlOrRd',
                        locations="uf",
                        featureidkey="properties.UF",
                        projection="mercator",
                        hover_data=['uf', 'ilesos'],
                        width=700)

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(title="Número de ilesos",
                                                lenmode="pixels", len=200))


    return container, fig


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)