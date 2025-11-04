import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np 
import plotly.graph_objects as go
from scipy.integrate import odeint

dash.register_page(__name__, path='/Clase_7', name='Clase_7')

layout = html.Div([

    html.Div([

        html.H2("Modelo SEIR - Epidemiología", className="title"),

        html.Div([
            html.Label("Población total (N) = "),
            dcc.Input(id="input-N", type='number', value=1000, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de transmisión (β): "),
            dcc.Input(id="input-beta", type='number', value=0.3, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de cambio a infeccioso (σ): "),
            dcc.Input(id="input-sigma", type='number', value=0.2, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de recuperación (ɣ):"),
            dcc.Input(id="input-gamma", type='number', value=0.1, step=0.01, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Infectados iniciales:"),
            dcc.Input(id="input-I0", type='number', value=1, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Expuestos iniciales:"),
            dcc.Input(id="input-E0", type='number', value=0, className="input-field")
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo de simulación: "),
            dcc.Input(id="input-tiempo", type='number', value=100, className="input-field")
        ], className="input-group"),

        html.Button("Simular Epidemia", id="btn-simular", className="btn-generar"),
    ], className="content left"),

    html.Div([
        html.H2("Gráfica de la Epidemia", className="title"),
        dcc.Graph(id="grafica-seir", style={"height": "450", "width": "100%"}),
    ], className="content right"),

], className="page-container")

def modelo_seir(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dS_dt = -beta * S * I / N
    dE_dt = beta * S * I / N - sigma * E
    dI_dt = sigma * E - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dE_dt, dI_dt, dR_dt]

@callback(
    Output("grafica-seir", "figure"),
    Input("btn-simular", "n_clicks"),
    State("input-N", "value"),
    State("input-beta", "value"),
    State("input-sigma", "value"),
    State("input-gamma", "value"),
    State("input-I0", "value"),
    State("input-E0", "value"),
    State("input-tiempo", "value"),
    prevent_initial_call=False
)
def simular_seir(n_clicks, N, beta, sigma, gamma, I0, E0, tiempo_max):
    S0 = N - I0 - E0
    R0 = 0
    y0 = [S0, E0, I0, R0]
    t = np.linspace(0, tiempo_max, 200)

    try:
        solucion = odeint(modelo_seir, y0, t, args=(N, beta, sigma, gamma))
        S, E, I, R = solucion.T
    except Exception:
        S = np.full_like(t, S0)
        E = np.full_like(t, E0)
        I = np.full_like(t, I0)
        R = np.full_like(t, R0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, 
        mode='lines', 
        name='Susceptibles (S)', 
        line=dict(
            color='blue', width=2),
        hovertemplate='Dia: %{x:.0f}<br>Susceptibles: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=E, 
        mode='lines', 
        name='Expuestos (E)', 
        line=dict(color='orange'),
        hovertemplate='Dia: %{x:.0f}<br>Expuestos: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=I, 
        mode='lines', 
        name='Infectados (I)', 
        line=dict(
            color='red'),
        hovertemplate='Dia: %{x:.0f}<br>Infectados: %{y:.0f}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=t, y=R, 
        mode='lines', 
        name='Recuperados (R)', 
        line=dict(
            color='green'),
        hovertemplate='Dia: %{x:.0f}<br>Recuperados: %{y:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text="<b>Evolución del modelo SEIR</b>",
            font=dict(
                size=20, 
                color='black'
            ),
            x=0.5, 
            y=0.98
        ),
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de Personas",
        paper_bgcolor='white',
        plot_bgcolor='lightyellow',
        font=dict(
            family="outfit", 
            size=12, 
            color="black"),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='black', 
        zeroline=True, zerolinecolor='black', zerolinewidth=2,
        )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='black', 
        zeroline=True, zerolinecolor='black', zerolinewidth=2
    )

    return fig