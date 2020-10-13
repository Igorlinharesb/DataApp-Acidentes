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

teste = [3, 2, 1, 1, 1, 1, 1, 2, 23, 3, 1]
teste2 = [2, 16, 5, 2, 1, 2, 1, 3, 3, 3, 7]

parameter_list=['dia_semana','causa_acidente','tipo_acidente','fase_dia','condicao_meteorologica','tipo_pista','tracado_via','uso_solo','pessoas','veiculos','mes']
 
input_variables=pd.DataFrame([teste2],columns=parameter_list,dtype=int)

prediction = lr_clf2.predict(input_variables)

print(prediction)
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
""" df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True) """