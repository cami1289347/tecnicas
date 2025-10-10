import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np 
import plotly.graph_objects as go

dash.register_page(__name__, path='/Clase_3', name='Clase_3')

layout= html.Div( children=[

    html.Div( children=[
        
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

        html.Button("Generar Gráfica", id="btn-general", className="btn-generar")
    ], className="content left"),

    html.Div(children=[
              
        html.H2("Gráfica", className="title"),

        dcc.Graph(
        id='Grafica-Poblacion',
         style={'height': '350px', 'width': '100%'},
        )
    ], className="content right")

], className="page-container")

@callback(
    Output('grafica-poblacion','figure'),
    Input('btn-generar','n_clicks'),
    State('input-p0', 'value'),
    State('input-r', 'value'),
    State('input-k', 'value'),
    State('input-t', 'value'),
    prevent_initial_call=False
)

def actualizar_grafica(n_clicks, P0, r, K, t_max):

    t=np.linspace(0, t_max, 20)

    P=(P0*K*np.exp(r*t))/((K-P0)+P0*np.exp(r*t))

    trace_poblacion=go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='P(t)',
        line=dict(
            color='blue',
            width=2
        ),
        marker=dict(
            size=6,
            color='black',
            symbol='circle'
        ),
        
    )