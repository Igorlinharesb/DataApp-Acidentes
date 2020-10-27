import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import joblib
from dash.dependencies import Input, Output, State
import base64
import flask
import glob
import os

# MODELO LR
model1 = open("LR_Classifier1.pkl", "rb")
model2 = open("LR_Classifier2.pkl", "rb")
lr_clf1 = joblib.load(model1)
lr_clf2 = joblib.load(model2)

# MODELO RF
model1 = open("RF_Classifier1.pkl", "rb")
model2 = open("RF_Classifier2.pkl", "rb")
rf_clf1 = joblib.load(model1)
rf_clf2 = joblib.load(model2)

# ÍCONES
iconp = '../img/pessoas.png'
iconp_base64 = base64.b64encode(open(iconp , 'rb').read()).decode('ascii')
iconv = '../img/veiculos.png'
iconv_base64 = base64.b64encode(open(iconv , 'rb').read()).decode('ascii')

# STYLESHEETS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# LISTAS - VALORES DE ATRIBUTOS
causes = ['Falta de atenção', 'Outras', 'Animais na pista', 'Defeito mecânico em veículo', 'Não guardar distância de segurança', 'Velocidade incompatível', 'Desobediência à sinalização', 'Ingestão de álcool', 'Defeito na via', 'Dormindo', 'Ultrapassagem indevida', 'Fenômenos da natureza', 'Avarias e/ou desgaste excessivo no pneu', 'Falta de atenção à condução', 'Desobediência às normas de trânsito pelo condutor', 'Restrição de visibilidade', 'Falta de atenção do pedestre', 'Condutor dormindo', 'Pista escorregadia', 'Sinalização da via insuficiente ou inadequada', 'Mal súbito', 'Carga excessiva e/ou mal acondicionada', 'Objeto estático sobre o leito carroçável', 'Deficiência ou não acionamento do sistema de iluminação/sinalização do veículo', 'Ingestão de substâncias psicoativas', 'Agressão externa', 'Desobediência às normas de trânsito pelo pedestre', 'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre']
tipo = ['Colisão frontal', 'Saída de pista', 'Atropelamento de animal', 'Capotamento', 'Colisão lateral', 'Atropelamento de pessoa', 'Colisão traseira', 'Colisão transversal', 'Tombamento', 'Colisão com objeto fixo', 'Danos eventuais', 'Queda de motocicleta/bicicleta/veículo', 'Derramamento de carga', 'Colisão com bicicleta', 'Colisão com objeto móvel', 'Incêndio', 'Queda de ocupante de veículo', 'Saída de leito carroçável', 'Colisão com objeto estático', 'Atropelamento de pedestre', 'Colisão com objeto em movimento', 'Engavetamento']
condicao = ['Céu claro', 'Chuva', 'Nublado', 'Sol', 'Nevoeiro/neblina', 'Vento', 'Granizo', 'Neve', 'Garoa/chuvisco']
tracado = ['Reta', 'Curva', 'Cruzamento', 'Interseção de vias', 'Rotatória', 'Desvio temporário', 'Viaduto', 'Ponte', 'Retorno regulamentado', 'Túnel']
meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

# APP LAYOUT
app.layout = html.Div(style={'width': '80%', 'margin': 'auto'}, children=[
    html.Br(),
    html.H1(children='Predição da gravidade de acidentes de trânsito',style={'textAlign': 'center'}),
    html.Br(),

    html.Div([

        html.Div([
            html.H6('Dia da semana'),
            dcc.Dropdown(
                id= 'dia_semana',
                options=[
                    {'label': 'Domingo', 'value': 1},
                    {'label': 'Segunda', 'value': 2},
                    {'label': 'Terça', 'value': 3},
                    {'label': 'Quarta', 'value': 4},
                    {'label': 'Quinta', 'value': 5},
                    {'label': 'Sexta', 'value': 6},
                    {'label': 'Sábado', 'value': 7}
                ],
                value=1
            ),
            html.Br(),
            html.H6('Causa do Acidente'),
            dcc.Dropdown(
                id='causa_acidente',
                options=[{'label': cause, 'value': i} for i, cause in enumerate(causes,1)],
                value=1
            ),
            html.Br(),
            html.H6('Tipo de Acidente'),
            dcc.Dropdown(
                id= 'tipo_acidente',
                options=[{'label': t, 'value': i} for i, t in enumerate(tipo,1)],
                value=1
            ),
            html.Br(),
            html.H6('Fase do dia'),
            dcc.Slider(
                id= 'fase_dia',
                min=1,
                max=4,
                marks={ 
                    1: {'label': 'pleno dia'},
                    2: {'label': 'plena noite'},
                    3: {'label': 'amanhecer'},
                    4: {'label': 'anoitecer'}
                },
                value=1,
            ),
            html.Br(),
            html.H6('Condição Metereológica'),
            dcc.Dropdown(
                id= 'condicao_meteorologica',
                options=[{'label': cond, 'value': i} for i, cond in enumerate(condicao,1)],
                value=1
            ),
            html.Br(),
            html.H6('Tipo de Pista'),
            dcc.Slider(
                id= 'tipo_pista',
                min=1,
                max=3,
                marks={ 
                    1: {'label': 'dupla'},
                    2: {'label': 'simples'},
                    3: {'label': 'múltipla'}
                },
                value=1,
            ),
            html.Br(),
            html.H6('Traçado da via'),
            dcc.Dropdown(
                id= 'tracado_via',
                options=[{'label': trac, 'value': i} for i, trac in enumerate(tracado,1)],
                value=1
            ),
            html.Br(),
            html.H6('Solo'),
            dcc.Slider(
                id= 'solo',
                min=1,
                max=3,
                marks={ 
                    1: {'label': 'rural'},
                    2: {'label': 'urbano'},
                    3: {'label': 'indefinido'}
                },
                value=1,
            ),
            html.Br(),
            html.H6('Quantidade de Pessoas'),
            dcc.Input(
                id="pessoas", type="number", placeholder="input with range",
                value=1,
            ),
            html.Br(),
            html.H6('Veículos'),
            dcc.Input(
                id="veiculos", type="number", placeholder="input with range",
                value=1,
            ),
            html.Br(),
            html.H6('Mês'),
            dcc.Dropdown(
                id= 'mes',
                options=[{'label': mes, 'value': i} for i, mes in enumerate(meses,1)],
                value=1
            ),
        ], className="four columns"),

        html.Div([
            html.Div(id='informacoes',style={'height': '250px', 'width': '100%','background-color': '#ffffff','border': '2px solid #aaaaaa','border-radius': '10px'},children=[
                
                html.H6(id='titulo', style={'padding-left': '20px','color':'#8d8d8d'},children='INFORMAÇÕES DO ACIDENTE:'),
                
                html.Div([
                    html.H6(id='info_met',children=''),
                ],className='two columns'),
                html.Div([
                    html.H2(id='info_dia',children='',style={'color':'#8d8d8d'}),
                    html.H4(id='info_mes',children='',style={'color':'#8d8d8d'}),
                    html.H6(id='info_fase',children=''),
                ],className='three columns'),
                
                html.Div([
                    html.H6(id='info_pista',children=''),
                    html.H6(id='info_via',children=''),
                    html.H6(id='info_solo',children=''),
                ],className='three columns'),
                html.Div([
                    html.H6(children='Causa:',style={'color':'#494949'}),
                    html.H6(id='info_causa',children='',style={'color':'#8d8d8d'}),
                    html.H6(children='Tipo:',style={'color':'#494949'}),
                    html.H6(id='info_tipo',children='',style={'color':'#8d8d8d'}),
                ],className='three columns'),
                
            ]),
            html.Div(style={'margin-top':'10px','height': '40px', 'width': '100%','background-color': '#ffffff','border-bottom': '2px solid #aaaaaa'},children=[
                
                html.Div([
                    html.H6(children='',style={'color':'#8d8d8d'}),
                ],className='seven columns'),
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(iconp_base64))
                ],className='one columns'),
                html.Div(children=[
                    html.H6(id='info_pessoas',children='',style={'color':'#8d8d8d'}),
                ],className='one columns'),
                
                html.Div(children=[
                    html.Img(src='data:image/png;base64,{}'.format(iconv_base64))

                ],className='one columns'),
                html.Div([
                    html.H6(id='info_veiculos',children='',style={'color':'#8d8d8d'}),
                ],className='one columns'),
            ]),

            html.H4('Modelo'),
            dcc.Dropdown(
                id= 'modelo',
                options=[
                    {'label': 'Logistic Regression', 'value': 1},
                    {'label': 'Random Forest', 'value': 2},
                ],
                value=1
            ), 
            html.Br(),
            dbc.Button( 
            id='submeter',
            n_clicks=0,
            children='Submeter',
            color='primary',
            block=True
            ),
            html.Br(),
            html.H1(id='result',children='',style={'textAlign': 'center'})
        ], className="eight columns")

    ]),
])


# CALLBACKS
@app.callback(
    Output('result','children'),
    [Input('submeter', 'n_clicks')],
    [State('dia_semana','value'),State('causa_acidente','value'),State('tipo_acidente','value'),
    State('fase_dia','value'),State('condicao_meteorologica','value'),State('tipo_pista','value'),
    State('tracado_via','value'), State('solo','value'), State('pessoas','value'), State('veiculos','value'),
    State('mes','value'),State('modelo','value')]
)
def update_predicao(n_clicks,dia_semana_value,causa_acidente_value,tipo_acidente_value,fase_dia_value,condicao_meteorologica_value,tipo_pista_value,tracado_via_value, solo_value,pessoas_value,veiculos_value,mes_value,modelo_value):
    
    # ESCOLHA DO MODELO DE CLASSIFICAÇÃO
    if modelo_value==1:
        # LR
        teste = [dia_semana_value,causa_acidente_value,tipo_acidente_value,fase_dia_value,condicao_meteorologica_value,tipo_pista_value,tracado_via_value, solo_value,pessoas_value,veiculos_value,mes_value]
        print(teste)
        parameter_list=['dia_semana','causa_acidente','tipo_acidente','fase_dia','condicao_meteorologica','tipo_pista','tracado_via','uso_solo','pessoas','veiculos','mes']
        input_variables=pd.DataFrame([teste],columns=parameter_list,dtype=int)
        prediction = lr_clf1.predict(input_variables)
        print(prediction)

    if modelo_value ==2:
        # RF
        teste = [dia_semana_value,causa_acidente_value,tipo_acidente_value,condicao_meteorologica_value, solo_value,pessoas_value,veiculos_value,mes_value]
        print(teste)
        parameter_list=['dia_semana','causa_acidente','tipo_acidente','condicao_meteorologica','uso_solo','pessoas','veiculos','mes']
        input_variables=pd.DataFrame([teste],columns=parameter_list,dtype=int)
        prediction = rf_clf1.predict(input_variables)
        print(prediction)

    # RESULTADO
    if (prediction==[1]) :

        test = '../img/acidentec1.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        )

    if (prediction==[2]) :

        test = '../img/acidentec2.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        )   
    
    if (prediction==[3]):

        test = '../img/acidentec3.png'
        test_base64 = base64.b64encode(open(test, 'rb').read()).decode('ascii')

        return html.Div([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(test_base64))
        ],  className="eight columns",
        ) 

@app.callback(
    Output('info_dia','children'),
    [Input('submeter','n_clicks')],
    [State('dia_semana','value')]
)
def update_dia_semana(n_clicks,dia_semana_value):
    dias = ['DOM','SEG','TER','QUA','QUI','SEX','SÁB']
    return dias[dia_semana_value-1]

@app.callback(
    Output('info_causa','children'),
    [Input('submeter','n_clicks')],
    [State('causa_acidente','value')]
)
def update_causa(n_clicks,causa_acidente_value):
    causa = ['Falta de atenção', 'Outras', 'Animais na pista', 'Defeito mecânico em veículo', 'Não guardar distância de segurança', 'Velocidade incompatível', 'Desobediência à sinalização', 'Ingestão de álcool', 'Defeito na via', 'Dormindo', 'Ultrapassagem indevida', 'Fenômenos da natureza', 'Avarias e/ou desgaste excessivo no pneu', 'Falta de atenção à condução', 'Desobediência às normas de trânsito pelo condutor', 'Restrição de visibilidade', 'Falta de atenção do pedestre', 'Condutor dormindo', 'Pista escorregadia', 'Sinalização da via insuficiente ou inadequada', 'Mal súbito', 'Carga excessiva e/ou mal acondicionada', 'Objeto estático sobre o leito carroçável', 'Deficiência de iluminação/sinalização do veículo', 'Ingestão de substâncias psicoativas', 'Agressão externa', 'Desobediência às normas de trânsito pelo pedestre', 'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre']
    return causa[causa_acidente_value-1]

@app.callback(
    Output('info_tipo','children'),
    [Input('submeter','n_clicks')],
    [State('tipo_acidente','value')]
)
def update_tipo(n_clicks,tipo_acidente_value):
    tipo = ['Colisão frontal', 'Saída de pista', 'Atropelamento de animal', 'Capotamento', 'Colisão lateral', 'Atropelamento de pessoa', 'Colisão traseira', 'Colisão transversal', 'Tombamento', 'Colisão com objeto fixo', 'Danos eventuais', 'Queda de veículo', 'Derramamento de carga', 'Colisão com bicicleta', 'Colisão com objeto móvel', 'Incêndio', 'Queda de ocupante de veículo', 'Saída de leito carroçável', 'Colisão com objeto estático', 'Atropelamento de pedestre', 'Colisão com objeto em movimento', 'Engavetamento']
    return tipo[tipo_acidente_value-1]

@app.callback(
    Output('info_fase','children'),
    [Input('submeter','n_clicks')],
    [State('fase_dia','value')]
)
def update_fase(n_clicks,fase_dia_value):
    fase = ['Pleno Dia','Plena Noite','Amanhecer','Anoitecer']
    return html.H5(id='info_fase',children='('+fase[fase_dia_value-1]+')',style={'color':'#8d8d8d'})

@app.callback(
    Output('info_met','children'),
    [Input('submeter','n_clicks')],
    [State('condicao_meteorologica','value')]
)
def update_condicao_met(n_clicks,condicao_meteorologica_value):
    condicao = ['ceu claro', 'chuva', 'nublado', 'sol', 'neblina', 'vento', 'granizo', 'neve', 'chuvisco']
    met = condicao[condicao_meteorologica_value-1]

    tempo = '../img/'+met+'.png'
    tempo_base64 = base64.b64encode(open(tempo, 'rb').read()).decode('ascii')

    return html.Div([
            html.Img(src='data:image/png;base64,{}'.format(tempo_base64))
        ],
        ) 

@app.callback(
    Output('info_pista','children'),
    [Input('submeter','n_clicks')],
    [State('tipo_pista','value')]
)
def update_tipo_pista(n_clicks,tipo_pista_value):
    pista = ['Dupla','Simples','Múltipla']
    return html.H6(id='info_pista',children='Pista: '+pista[tipo_pista_value-1],style={'color':'#8d8d8d'}), 

@app.callback(
    Output('info_via','children'),
    [Input('submeter','n_clicks')],
    [State('tracado_via','value')]
)
def update_via(n_clicks,tracado_via_value):
    tracado = ['Reta', 'Curva', 'Cruzamento', 'Interseção de vias', 'Rotatória', 'Desvio temporário', 'Viaduto', 'Ponte', 'Retorno regulamentado', 'Túnel']
    return html.H6(id='info_via',children='Via: '+tracado[tracado_via_value-1],style={'color':'#8d8d8d'})

@app.callback(
    Output('info_solo','children'),
    [Input('submeter','n_clicks')],
    [State('solo','value')]
)
def update_solo(n_clicks,solo_value):
    solos = ['Rural','Urbano','Indefinido']
    return html.H6(id='info_solo',children='Zona: '+solos[solo_value-1],style={'color':'#8d8d8d'})

@app.callback(
    Output('info_pessoas','children'),
    [Input('submeter','n_clicks')],
    [State('pessoas','value')]
)
def update_pessoas(n_clicks,pessoas_value):
    return html.H6(id='info_pessoas',children=pessoas_value,style={'color':'#8d8d8d'}) 

@app.callback(
    Output('info_veiculos','children'),
    [Input('submeter','n_clicks')],
    [State('veiculos','value')]
)
def update_veiculos(n_clicks,veiculos_value):
    return html.H6(id='info_veiculos',children=veiculos_value,style={'color':'#8d8d8d'})

@app.callback(
    Output('info_mes','children'),
    [Input('submeter','n_clicks')],
    [State('mes','value')]
)
def update_mes(n_clicks,mes_value):
    meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    return meses[mes_value-1]



if __name__ == '__main__':
    app.run_server(debug=True)