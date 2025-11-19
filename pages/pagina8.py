
import dash
from dash import html, dcc, Output, Input, State, callback
import numpy as np 
import plotly.graph_objects as go
from scipy.integrate import odeint
import requests
from datetime import datetime

dash.register_page(__name__, path='/Clase_8', name='Covid_19')

layout = html.Div([

    html.Div([

        html.H2("DashBoard Covid-19", className="title"),

        html.Div([
           html.Label("Seleccione el pais: "),
              dcc.Dropdown(
                id="dropdown-pais",
                options=[
                    {"label": "Peru", "value": "Peru"},
                    {"label": "México", "value": "Mexico"},
                    {"label": "Estados Unidos", "value": "USA"},
                    {"label": "Canada", "value": "Canada"},
                    {"label": "Brasil", "value": "Brazil"},
                    {"label": "Argentina", "value": "Argentina"},
                    {"label": "Colombia", "value": "Colombia"},
                    {"label": "Chile", "value": "Chile"},
                ],
                value="Peru",
                className="input-field",
                style={"width": "100%"},
              )
        ], className="input-group"),

        html.Div([
            html.Label("Dias historico:"),

            dcc.Dropdown(
                id="dropdown-dias-covid",
                options=[
                    {"label": "30 dias", "value": 30},
                    {"label": "60 dias", "value": 60},
                    {"label": "90 dias", "value": 90},
                    {"label": "Todo el historico", "value": "all"},
                ],
                value=30,
                className="input-field",
                style={"width": "100%"},
            )
        ], className="input-group"),

    html.Button("Actualizar Datos", id="btn-actualizar-covid", className="btn-generar"),

    html.Div(
        id="info-actualizado-covid",
    )
    ], className="content left"),


    html.Div([

        html.H2("Estadisticas en tiempo real", className="title"),

        html.Div([
            html.Div([
                html.H4("Total de Casos: ", style={'color': "#FC5FFC"}),
                html.H3(id="total-casos", style={'color': 'blue'}),

            ], style={
                "background-color": "#F0F8FF",
                "padding": "10px",
                "border-radius": "10px",
                "text-align": "center",
                "margin": "5px"
                }),
            
            html.Div([
                html.H4("Casos nuevos: ", style={'color': "#FC5FFC"}),
                html.H3(id="casos-nuevos", style={'color': 'blue'}),

            ], style={
                "background-color": "#F0F8FF",
                "padding": "10px",
                "border-radius": "10px",
                "text-align": "center",
                "margin": "5px"
                }),
            
            html.Div([
                html.H4("Total muertes: ", style={'color': "#FC5FFC"}),
                html.H3(id="total-muertes", style={'color': 'blue'}),

            ], style={
                "background-color": "#F0F8FF",
                "padding": "10px",
                "border-radius": "10px",
                "text-align": "center",
                "margin": "5px"
                }),

            html.Div([
                html.H4("Total recuperados: ", style={'color': "#FC5FFC"}),
                html.H3(id="total-recuperados", style={'color': 'blue'}),

            ], style={
                "background-color": "#F0F8FF",
                "padding": "10px",
                "border-radius": "10px",
                "text-align": "center",
                "margin": "5px"
                })
            

        ], style={
                "display": "flex"}),
            dcc.Graph(id="grafica-covid", style={"height":"450", "width":"100%"}),

    ], className="content right")

], className="page-container")

#Funciones para conectar a la API 
def obtener_datos_covid(pais):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{pais}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos del pais {pais}: {e}")
        return None

def obtener_historico_covid(pais, dias):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{pais}"
        params={"lastdays": dias}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al obtener historico del pais {pais}: {e}")
        return None

def formatear_numero(num):
    try:
        return f"{num:,}"
    except (ValueError, TypeError):
        return "N/A"
    
@callback(
    Output("total-casos", "children"),
    Output("casos-nuevos", "children"),
    Output("total-muertes", "children"),
    Output("total-recuperados", "children"),
    Output("grafica-covid", "figure"),
    Output("info-actualizado-covid", "children"),
    Input("btn-actualizar-covid", "n_clicks"),
    State("dropdown-pais", "value"),
    State("dropdown-dias-covid", "value"),
    prevent_initial_call=False
)

def actualizar_datos_covid(n_clicks, pais, dias):

    datos_actuales = obtener_datos_covid(pais)
    historico = obtener_historico_covid(pais, dias)

    if not datos_actuales or not historico:
        fig= go.Figure()
        fig.add_annotation(
            text="Error al obtener datos",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=15, color="red")
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        return "N/A", "N/A", "N/A", "N/A" , fig, "No se pudieron actualizar los datos."
    
    total_casos= datos_actuales.get("cases", 0)
    casos_hoy= datos_actuales.get("todayCases", 0)
    total_recuperados= datos_actuales.get("recovered", 0)
    total_muertes= datos_actuales.get("deaths", 0)

    total_casos_texto= formatear_numero(total_casos)
    casos_hoy_texto= formatear_numero(casos_hoy)
    total_recuperados_texto= formatear_numero(total_recuperados)
    total_muertes_texto= formatear_numero(total_muertes)

    timeline=historico.get("timeline", {})
    casos_historico= timeline.get("cases", {})
    muertes_historicas= timeline.get("deaths", {})

    fechas= list(casos_historico.keys())
    valores_casos= list(casos_historico.values())
    valores_muertes= list(muertes_historicas.values())

    fechas_dt = [datetime.strptime(fecha, "%m/%d/%y") for fecha in fechas]

    fig= go.Figure()

    fig.add_trace(go.Scatter(
        x=fechas_dt, 
        y=valores_casos,
        mode='lines',
        name='Casos Totales',
        line=dict(color='blue', width=2),
        hovertemplate='Fecha: %{x|%Y-%m-%d}<br>Casos: %{y:,}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=fechas_dt,
        y=valores_muertes,
        mode='lines',
        name='Muertes Totales',
        line=dict(color='red', width=2),
        hovertemplate='Fecha: %{x|%Y-%m-%d}<br>Muertes: %{y:,}<extra></extra>'
    ))

    return [total_casos_texto, casos_hoy_texto, total_muertes_texto, total_recuperados_texto, fig, f"Datos actualizados para {pais}" ]