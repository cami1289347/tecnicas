import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np 
import plotly.graph_objects as go
from utils.funciones import fucion_graficas_ecu_log

dash.register_page(__name__, path='/Clase_4', name='Clase_4')

layout= html.Div( children=[

    html.Div( children=[
        
        html.H2("Gráfica", className="title"),

        dcc.Graph(
        id='grafica',
         style={'height': '350px', 'width': '100%'},
        )
        
    ], className="content"),

    html.Div(children=[
    
     html.H2("Parametros del modelo", className="title"),

        html.Div([
            html.Label("Poblacion inicial P(0):"),
            dcc.Input(id="input-p0", type="number", value=200, className="input-field")
        ], className="input-group"),

        html.Div([
        html.Label("Tasa de Crecimiento (r):"),
        dcc.Input(id="input-r", type="number", value=0.04, className="input-field")

        ], className="input-group"),

        html.Div([
        html.Label("Capacidad de Carga (K):"),
        dcc.Input(id="input-k", type="number", value=750, className="input-field")
        ], className="input-group"),

        html.Div([
        html.Label("Tiempo Máximo (t):"),
        dcc.Input(id="input-t", type="number", value=100, className="input-field")
        ], className="input-group"),

        html.Button("Generar Gráfica", id="btn-generar", className="btn-generar")
     
    ], className="content right")

], className="page-container")

@callback(
    Output('grafica', 'figure'),
    Input('btn-generar', 'n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=True  
)
def update_graph(n_clicks, p0, r, k, t_max):
    
    fig = fucion_graficas_ecu_log(P0=p0, K=k, t_max=t_max, r=r)
    
    return fig
