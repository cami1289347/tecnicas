import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


P0 = 100
r = 0.15
K = 1000
t = np.linspace(0, 100, 100)

# Ecuación logística: P(t) = K / (1 + ((K - P0)/P0) * e^(-rt))
P_logistica = K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# Trazo de la curva logística
trace_logistica = go.Scatter(
    x=t,
    y=P_logistica,
    mode='lines',
    line=dict(color='blue', width=3),
    hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
)

# Línea horizontal de capacidad de carga
trace_capacidad = go.Scatter(
    x=t,
    y=[K]*len(t),
    mode='lines',
    line=dict(color='red', dash='dash'),
    hoverinfo='skip',
)

# Crear figura con ambas curvas
fig = go.Figure(data=[trace_logistica, trace_capacidad])

fig.update_layout(
    title=dict(
        text='<b>Crecimiento poblacional logístico</b>',
        font=dict(size=20, color='black'),
        x=0.5,
        y=0.93
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=50, b=40),
    paper_bgcolor='lightblue',
    plot_bgcolor='white',
    font=dict(family='Outfit', size=11, color='black'),
    showlegend=False  
)


fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True
)

fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True
)

dash.register_page(__name__, path='/Clase_2', name='Clase_2')

layout = html.Div(children= [
    html.Div(children=[
        html.H2("Gráfica", className="title"),

        dcc.Graph(
            figure=fig,
            style={'height': '350px', 'width':'100%'}
            )
    ], className="content" ),

    html.Div(children=[
        html.H2("Crecimiento poblacional Logistico", className="title"),
            dcc.Markdown("""El crecimiento exponencial se produce cuando una población crece muy rápidamente durante un período corto de tiempo. 
            Cuando el crecimiento de la población comienza a estabilizarse, se denomina crecimiento logístico . 
            A medida que el crecimiento de la población se vuelve más restringido y el tamaño de la población alcanza la estabilidad, 
            esa población alcanza su capacidad de carga. Sea $K$ la capacidad de carga para un organismo particular en un entorno dado, 
            y sea $r$ un número real que representa la tasa de crecimiento. La función $P(t)$ representa la población de este organismo como función del tiempo $t$, 
            y la constante $P₀$ representa la población inicial (la población del organismo en el tiempo $t = 0$). Entonces, la ecuación diferencial logística es: 
            $$\\frac{dP}{dt} = rP\\left(1 - \\frac{P}{K}\\right)$$ """ , mathjax=True),

            
            dcc.Markdown(""" Resolviento la EDO obtenemos: $$P(t) = \\frac{K}{1 + \\left(\\frac{K - P_0}{P_0}\\right)e^{-rt}}$$. 
            Por ejemplo si tomamos como parametros:  $P_0=100$, $r=0.15$ y$k=1000$.
            """, mathjax=True),

    ], className="content right" )


], className="page-container")