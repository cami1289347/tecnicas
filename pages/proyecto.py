import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np 
import plotly.graph_objects as go
from scipy.integrate import solve_ivp  # Importamos solve_ivp

dash.register_page(__name__, path='/Proyecto', name='Proyecto')

# Definición del Sistema de Ecuaciones Diferenciales
def sistema_sip(t, y, params):
    xS, xI, y_pred = y

    r = params['r']
    K = params['K']
    alpha = params['alpha']
    g = params['g']
    a1 = params['a1']
    m = params['m']
    mu = params['mu']
    rho = params['rho']
    a2 = params['a2']
    n = params['n']
    w1 = params['w1']
    w2 = params['w2']
    c = params['c']
    d = params['d']

    
    dxS_dt = r * xS * (1 - (xS + xI) / K) - alpha * xS * xI + g * xI - a1 * (1 - m) * xS * y_pred - mu * xS
    dxI_dt = alpha * xS * xI - (mu + g + rho) * xI - a2 * (1 - n) * xI * y_pred
    dy_dt = a1 * w1 * (1 - m) * xS * y_pred + a2 * w2 * (1 - n) * xI * y_pred - c * y_pred - d * y_pred**2

    return [dxS_dt, dxI_dt, dy_dt]


DEFAULT_PARAMS = {
    "r": {"label": "Crecimiento intrínseco (r)", "value": 0.10, "step": 0.01},
    "K": {"label": "Capacidad de carga (K)", "value": 60.0, "step": 1.0},
    "alpha": {"label": "Tasa de infección (α)", "value": 0.30, "step": 0.01},
    "g": {"label": "Tasa de recuperación (g)", "value": 0.07, "step": 0.005},
    "a1": {"label": "Tasa de encuentro (S) (a₁)", "value": 0.20, "step": 0.01},
    "m": {"label": "Refugio (S) (m)", "value": 0.60, "step": 0.01},
    "mu": {"label": "Mortalidad natural (μ)", "value": 0.01, "step": 0.001},
    "rho": {"label": "Mortalidad extra por enf. (ρ)", "value": 0.10, "step": 0.01},
    "a2": {"label": "Tasa de encuentro (I) (a₂)", "value": 0.30, "step": 0.01},
    "n": {"label": "Refugio (I) (n)", "value": 0.40, "step": 0.01},
    "w1": {"label": "Efic. depredación (S)  (w₁)", "value": 0.45, "step": 0.01},
    "w2": {"label": "Efic. depredación (I)  (w₂)", "value": 0.40, "step": 0.01},
    "c": {"label": "Mortalidad Depredador (c)", "value": 0.035, "step": 0.001},
    "d": {"label": "Competencia Depredador (d)", "value": 0.01, "step": 0.001},
}

INITIAL_CONDITIONS = {
    "xS0": {"label": "Presas Susceptibles Iniciales (xS₀)", "value": 12.0, "step": 0.1},
    "xI0": {"label": "Presas Infectadas Iniciales (xI₀)", "value": 3.0, "step": 0.1},
    "y0": {"label": "Depredadores Iniciales (y₀)", "value": 7.0, "step": 0.1},
    "tiempo": {"label": "Tiempo de simulación", "value": 1000, "step": 10},
}


def generate_input_group(id_key, config):
    return html.Div([
        html.Label(config["label"]),
        dcc.Input(
            id=f"input-{id_key}",
            type='number',
            value=config["value"],
            step=config["step"],
            className="input-field"
        )
    ], className="input-group")


layout = html.Div([

    html.Div([

        html.H2("Modelo Depredador-Presa-Enfermedad", className="title"),
        html.H3("Parámetros del Sistema", className="subtitle"),

        # Contenedor para los 14 inputs de Parámetros
        html.Div([
            *[generate_input_group(key, config) for key, config in DEFAULT_PARAMS.items()]
        ], className="input-grid-params"),  # Usamos un grid para organizarlos

        html.H3("Condiciones Iniciales y Tiempo", className="subtitle", style={'marginTop': '20px'}),

        # Contenedor para las 4 condiciones iniciales/tiempo
        html.Div([
            *[generate_input_group(key, config) for key, config in INITIAL_CONDITIONS.items()]
        ], className="input-grid-init"),

        html.Button("Simular Dinámica Poblacional", id="btn-simular", className="btn-generar", style={'marginTop': '30px', 'marginBottom': '20px'}),

    ], className="content left"),

    html.Div([
        html.H2("Gráfica de la Dinámica Poblacional", className="title", style={'marginBottom': '10px'}),  
        dcc.Graph(id="grafica-sip", style={"height": "650px", "width": "100%"}),
    ], className="content right"),


], className="page-container")


all_states = [
    State("input-xS0", "value"),
    State("input-xI0", "value"),
    State("input-y0", "value"),
    State("input-tiempo", "value"),
]

for key in DEFAULT_PARAMS.keys():
    all_states.append(State(f"input-{key}", "value"))

@callback(
    Output("grafica-sip", "figure"),
    Input("btn-simular", "n_clicks"),
    all_states,  
    prevent_initial_call=False
)

def simular_sip(n_clicks, xS0, xI0, y0, tiempo_max, r, K, alpha, g, a1, m, mu, rho, a2, n, w1, w2, c, d):
    
    params = {
        'r': r, 'K': K, 'alpha': alpha, 'g': g, 'a1': a1, 'm': m, 'mu': mu, 'rho': rho,
        'a2': a2, 'n': n, 'w1': w1, 'w2': w2, 'c': c, 'd': d,
    }

    # Condiciones iniciales y tiempo
    y0_vec = [xS0, xI0, y0]
    t_span = [0, tiempo_max]
    t_eval = np.linspace(0, tiempo_max, 2000)

    try:
       
        solucion = solve_ivp(
            sistema_sip, 
            t_span, 
            y0_vec, 
            t_eval=t_eval, 
            method='RK45', 
            args=(params,) 
        )
        xS, xI, y_pred = solucion.y
        t = solucion.t
    except Exception as e:
        print(f"Error en solve_ivp: {e}")
        # En caso de error, retornar una gráfica vacía o con valores iniciales
        t = np.linspace(0, tiempo_max, 2000)
        xS, xI, y_pred = np.full_like(t, xS0), np.full_like(t, xI0), np.full_like(t, y0)


    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=xS, mode='lines', 
        name='Presas Susceptibles (xS)', 
        line=dict(color='green', width=2),
        hovertemplate='Tiempo: %{x:.0f}<br>xS: %{y:.2f}<extra></extra>'
    )) 

    fig.add_trace(go.Scatter(
        x=t, y=xI, mode='lines', 
        name='Presas Infectadas (xI)', 
        line=dict(color='red', width=2),
        hovertemplate='Tiempo: %{x:.0f}<br>xI: %{y:.2f}<extra></extra>'
    )) 

    fig.add_trace(go.Scatter(
        x=t, y=y_pred, mode='lines', 
        name='Depredadores (y)', 
        line=dict(color='blue', width=2),
        hovertemplate='Tiempo: %{x:.0f}<br>y: %{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=[t[-1]], y=[xS[-1]], mode='markers', name='xS Final', 
        marker=dict(color='green', size=8), showlegend=False,
        hovertemplate=f"xS Final: {xS[-1]:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[t[-1]], y=[xI[-1]], mode='markers', name='xI Final', 
        marker=dict(color='red', size=8), showlegend=False,
        hovertemplate=f"xI Final: {xI[-1]:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=[t[-1]], y=[y_pred[-1]], mode='markers', name='y Final', 
        marker=dict(color='blue', size=8), showlegend=False,
        hovertemplate=f"y Final: {y_pred[-1]:.2f}<extra></extra>"
    ))

    fig.update_layout(
        title="<b>Simulación del Sistema Depredador-Presa-Enfermedad</b>",  
        xaxis_title="Tiempo",
        yaxis_title="Densidad de Población",
        plot_bgcolor='lightyellow',
        paper_bgcolor='White',
        font=dict(family="Arial", size=12, color="black"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0), 
        margin=dict(l=40, r=40, t=100, b=40)  
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
