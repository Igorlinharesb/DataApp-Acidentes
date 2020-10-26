import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import joblib


model1 = open("LR_Classifier1.pkl", "rb")
model2 = open("LR_Classifier2.pkl", "rb")

lr_clf1 = joblib.load(model1)
lr_clf2 = joblib.load(model2)

teste = [1, 6, 1, 1, 2, 2, 0, 3, 6, 3, 2]
teste2 = [2, 16, 5, 2, 1, 2, 1, 3, 3, 3, 7]

parameter_list=['dia_semana','causa_acidente','tipo_acidente','fase_dia','condicao_meteorologica','tipo_pista','tracado_via','uso_solo','pessoas','veiculos','mes']
 
input_variables=pd.DataFrame([teste],columns=parameter_list,dtype=int)

prediction = lr_clf2.predict(input_variables)

print(prediction)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})



causes = ['falta de atenção', 'outras', 'animais na pista', 'defeito mecânico em veículo', 'não guardar distância de segurança', 'velocidade incompatível', 'desobediência à sinalização', 'ingestão de álcool', 'defeito na via', 'dormindo', 'ultrapassagem indevida', 'fenômenos da natureza', 'avarias e/ou desgaste excessivo no pneu', 'falta de atenção à condução', 'desobediência às normas de trânsito pelo condutor', 'restrição de visibilidade', 'falta de atenção do pedestre', 'condutor dormindo', 'pista escorregadia', 'sinalização da via insuficiente ou inadequada', 'mal súbito', 'carga excessiva e/ou mal acondicionada', 'objeto estático sobre o leito carroçável', 'deficiência ou não acionamento do sistema de iluminação/sinalização do veículo', 'ingestão de substâncias psicoativas', 'agressão externa', 'desobediência às normas de trânsito pelo pedestre', 'ingestão de álcool e/ou substâncias psicoativas pelo pedestre']
tipo = ['colisão frontal', 'saída de pista', 'atropelamento de animal', 'capotamento', 'colisão lateral', 'atropelamento de pessoa', 'colisão traseira', 'colisão transversal', 'tombamento', 'colisão com objeto fixo', 'danos eventuais', 'queda de motocicleta/ bicicleta/ veículo', 'derramamento de carga', 'colisão com bicicleta', 'colisão com objeto móvel', 'incêndio', 'queda de ocupante de veículo', 'saída de leito carroçável', 'colisão com objeto estático', 'atropelamento de pedestre', 'colisão com objeto em movimento', 'engavetamento']
condicao = ['ceu claro', 'chuva', 'nublado', 'sol', 'nevoeiro/neblina', 'vento', 'granizo', 'neve', 'garoa/chuvisco']
tracado = ['reta', 'curva', 'cruzamento', 'interseção de vias', 'rotatória', 'desvio temporário', 'viaduto', 'ponte', 'retorno regulamentado', 'túnel']
meses = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(style={'width': '80%', 'margin': 'auto'}, children=[
    html.Br(),
    html.H1(children='Predição de acidentes fatais',style={'textAlign': 'center'}),
    html.Br(),

    html.Div([

        html.Div([
            html.H6('Dia da semana'),
            dcc.Dropdown(
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
                options=[{'label': cause, 'value': i} for i, cause in enumerate(causes,1)],
                value=1
            ),
            html.Br(),
            html.H6('Tipo de Acidente'),
            dcc.Dropdown(
                options=[{'label': t, 'value': i} for i, t in enumerate(tipo,1)],
                value=1
            ),
            html.Br(),
            html.H6('Fase do dia'),
            dcc.Slider(
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
                options=[{'label': cond, 'value': i} for i, cond in enumerate(condicao,1)],
                value=1
            ),
            html.Br(),
            html.H6('Tipo de Pista'),
            dcc.Slider(
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
                options=[{'label': trac, 'value': i} for i, trac in enumerate(tracado,1)],
                value=1
            ),
            html.Br(),
            html.H6('Solo'),
            dcc.Slider(
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
                id="pessoa", type="number", placeholder="input with range",
            ),
            html.Br(),
            html.H6('Veículos'),
            dcc.Input(
                id="veiculo", type="number", placeholder="input with range",
            ),
            html.Br(),
            html.H6('Mês'),
            dcc.Dropdown(
                options=[{'label': mes, 'value': i} for i, mes in enumerate(meses,1)],
                value=1
            ),
            html.Br(),
        ], className="four columns"),

        html.Div([
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ], className="eight columns")

    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)