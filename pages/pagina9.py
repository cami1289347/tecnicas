import dash
from dash import html, dcc, Output, Input, State, callback
import pandas as pd
from dash import dash_table
import plotly.graph_objects as go
import plotly.express as px
import requests
from datetime import date, timedelta


API_KEY = 'g8cg0goL2pwFnGKMP3O4BH7BYDD2DxuLeIXfSFdx' 

dash.register_page(__name__, path='/neo_dashboard', name='NeoWs Dashboard')

def obtener_datos_neos(dias):
    """Obtiene datos de asteroides (NEOs) de la API de la NASA para un rango de días."""
    try:
        if dias == 'max': # Opción para rango largo (simulando "Todo el histórico" para la API Feed)
            dias = 7 # La API Feed solo permite un máximo de 7 días entre start_date y end_date
            
        end_date = date.today()
        start_date = end_date - timedelta(days=dias)
        
        url = (f"https://api.nasa.gov/neo/rest/v1/feed?"
               f"start_date={start_date.strftime('%Y-%m-%d')}&"
               f"end_date={end_date.strftime('%Y-%m-%d')}&"
               f"api_key={API_KEY}")
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la API NeoWs: {e}")
        return pd.DataFrame(), f"Error de conexión: {e}"

    neos = []
    # Itera sobre los datos por fecha
    for date_str, neo_list in data.get('near_earth_objects', {}).items():
        for neo in neo_list:
            # Solo consideramos el primer acercamiento si hay múltiples
            close_approach = neo['close_approach_data'][0]
            
            neos.append({
                'id': neo['id'],
                'nombre': neo['name'],
                'es_peligroso': neo['is_potentially_hazardous_asteroid'],
                'diametro_max_km': neo['estimated_diameter']['kilometers']['estimated_diameter_max'],
                'distancia_lunar': float(close_approach['miss_distance']['lunar']),
                'velocidad_km_s': float(close_approach['relative_velocity']['kilometers_per_second']),
                'fecha_cercana': close_approach['close_approach_date_full']
            })
            
    df = pd.DataFrame(neos)
    # Prepara la columna 'es_peligroso' para visualización
    df['es_peligroso_str'] = df['es_peligroso'].apply(lambda x: 'Sí' if x else 'No')
    
    return df, f"Datos actualizados para el rango: {start_date} a {end_date}"


def formatear_numero(num):
    """Formatea números grandes con comas."""
    try:
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return "N/A"

layout = html.Div([

    # Contenedor de Controles y Tabla (Izquierda) - 50% de ancho (flex: 1)
    html.Div([

        html.H2("☄️ Control y Detalle de Asteroides (NeoWs)", className="title"),

        html.Div([
            html.Label("Seleccione el rango de días (máx. 7): "),
            dcc.Dropdown(
                id="dropdown-dias-neos",
                options=[
                    {"label": "3 días", "value": 3},
                    {"label": "4 días", "value": 4},
                    {"label": "5 días", "value": 5},
                    {"label": "6 días", "value": 6},
                    {"label": "7 días ", "value": 7},
                ],
                value=7,
                className="input-field",
                style={"width": "100%"},
            )
        ], className="input-group"),
        
        html.Button("Actualizar Datos de Asteroides", id="btn-actualizar-neos", className="btn-generar", style={'marginTop': '10px', 'marginBottom': '20px'}),

        html.Div(
            id="info-actualizado-neos",
            style={'marginTop': '10px', 'color': 'black', 'fontWeight': 'bold'}
        ),

        html.H3("Tabla de Detalle de Objetos Cercanos a la Tierra", 
                    style={'marginTop': '10px', 'marginBottom': '10px', 'fontSize': '1.3em', 'color': 'black'}),
        
        # Envolver la tabla en un div para controlar el overflow
        html.Div([
            dash_table.DataTable(
                id='tabla-neos',
                columns=[
                    {"name": "Nombre", "id": "nombre"},
                    {"name": "Diámetro Máx. (km)", "id": "diametro_max_km", "type": "numeric", 
                     "format": dash_table.Format.Format(precision=3, scheme=dash_table.Format.Scheme.fixed)},
                    {"name": "Peligroso", "id": "es_peligroso_str"},
                    {"name": "Dist. Lunar", "id": "distancia_lunar", "type": "numeric", 
                     "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)},
                    {"name": "Velocidad (km/s)", "id": "velocidad_km_s", "type": "numeric", 
                     "format": dash_table.Format.Format(precision=2, scheme=dash_table.Format.Scheme.fixed)},
                    {"name": "Fecha Cercana", "id": "fecha_cercana"}
                ],
                data=[],
                sort_action="native",
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #ddd',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    "textAlign": "center",
                    'width': '100%',  # Asegurar que la tabla ocupe el 100% del contenedor
                    'minWidth': '600px'  # Mínimo ancho para evitar que se comprima demasiado
                },
                style_header={
                    'backgroundColor': '#003366', 
                    'color': 'white', 
                    'fontWeight': 'bold',
                    'fontSize': '0.9em',
                    'textAlign': 'center'
                },
                style_cell={
                    'fontFamily': 'Inter, sans-serif',
                    'textAlign': 'center',
                    'padding': '8px',
                    'fontSize': '0.85em',
                    'minWidth': '80px',  # Mínimo ancho por celda para evitar compresión excesiva
                    'maxWidth': '150px',  # Máximo ancho para controlar expansión
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
                style_data_conditional=[
                    { # Estilo para filas peligrosas
                        'if': {'filter_query': '{es_peligroso_str} = "Sí"'},
                        'backgroundColor': '#FFEBEE', # Rojo pálido suave
                        'color': '#D32F2F',          # Rojo oscuro para el texto
                        'fontWeight': 'bold'
                    },
                    { # Estilo para la columna de Peligroso
                        'if': {'column_id': 'es_peligroso_str'},
                        'textAlign': 'center'
                    }
                ],
                page_action='native',
                page_current=0,
                page_size=10, 
                export_format='csv'
            )
        ], style={'width': '100%', 'overflowX': 'auto'})  # Div envolvente para scroll horizontal si es necesario

    ], className="content left", style={'flex': '1', 'padding': '15px', 'backgroundColor': '#f8f9fa'}),  # Reducido padding a 15px


    html.Div([

        html.H2("Estadísticas y Gráficos Clave", className="title"),

        # Tarjetas de Resumen
        html.Div([
            html.Div([
                html.H4("Total de NEOs Encontrados:", 
                        style={'color': "#003366"}
                        ),
                html.H3(id="total-neos", 
                        style={'color': "#007bff"}
                        ),
            ], className="card-summary", style={
                'flex': '1',
                'margin': '5px',
                'padding': '10px',
                'borderRadius': '8px', 
                'backgroundColor': '#E6F0FF', 
                'textAlign': 'center',
                'minHeight': '120px',  # Añadido para uniformizar el tamaño de las tarjetas
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
                }
            ),
            
            html.Div([
                html.H4("Potencialmente Peligrosos:", style={'color': "#CC0000"}),
                html.H3(id="peligrosos-count", style={'color': "#FF4136"}),
            ], className="card-summary", style={
                'flex': '1',
                'margin': '5px', 
                'padding': '10px', 
                'borderRadius': '8px', 
                'backgroundColor': '#FFE6E6', 
                'textAlign': 'center',
                'minHeight': '120px',  # Añadido para uniformizar el tamaño de las tarjetas
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
                }
            ),
            
            html.Div([
                html.H4("Diámetro Promedio:", style={'color': "#006600"}),
                html.H3(id="diametro-promedio", style={'color': "#2ECC40"}),
            ], className="card-summary", style={
                'flex': '1',
                'margin': '5px', 
                'padding': '10px', 
                'borderRadius': '8px', 
                'backgroundColor': '#E6FFE6', 
                'textAlign': 'center',
                'minHeight': '120px',  # Añadido para uniformizar el tamaño de las tarjetas
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
                }
            ),

            html.Div([
                html.H4("Máx. Velocidad:", style={'color': "#FF8C00"}),
                html.H3(id="velocidad-maxima", style={'color': "#FFD700"}),
            ], className="card-summary", style={    
                'flex': '1',
                'margin': '5px', 
                'padding': '10px', 
                'borderRadius': '8px', 
                'backgroundColor': '#FFF5E6', 
                'textAlign': 'center',
                'minHeight': '120px',  # Añadido para uniformizar el tamaño de las tarjetas
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
                }
            ),
            
        ], style={
            "display": "flex", 
            "justify-content": "space-between", 
            'marginBottom': '30px'
        }),
        
        # Gráfico principal: Velocidad vs. Distancia
        dcc.Graph(id="grafica-neos-scatter", style={"height": "450px", "width": "100%"}),

    ], className="content right", style={'flex': '1','padding': '15px'})  # Reducido padding a 15px

], className="page-container", style={'display': 'flex', 'flexDirection': 'row'})


@callback(
    Output("total-neos", "children"),
    Output("peligrosos-count", "children"),
    Output("diametro-promedio", "children"),
    Output("velocidad-maxima", "children"),
    Output("grafica-neos-scatter", "figure"),
    Output("info-actualizado-neos", "children"),
    Output("tabla-neos", "data"),
    Input("btn-actualizar-neos", "n_clicks"),
    State("dropdown-dias-neos", "value"),
    prevent_initial_call=False
)

def actualizar_datos_neos(n_clicks, dias):
    
    df, mensaje_actualizacion = obtener_datos_neos(dias)

    error_fig = go.Figure().add_annotation(
        text="Error: No hay datos o fallo de conexión con la API.",
        xref="paper", 
        yref="paper", 
        x=0.5, 
        y=0.5, 
        showarrow=False, 
        font=dict(
            size=16, 
            color="red",        
            family="Montserrat"
        ),
    ).update_layout(paper_bgcolor="#EFEFEF", plot_bgcolor="#EFEFEF")

    if df.empty:
        return "N/A", "N/A", "N/A", "N/A", error_fig, mensaje_actualizacion, []
    
    total_neos = len(df)
    peligrosos_count = len(df[df['es_peligroso'] == True])
    diametro_promedio = df['diametro_max_km'].mean() if not df['diametro_max_km'].empty else 0
    velocidad_maxima = df['velocidad_km_s'].max() if not df['velocidad_km_s'].empty else 0

    fig = px.scatter(
        df,
        x='distancia_lunar',
        y='velocidad_km_s',
        color='es_peligroso_str',
        size='diametro_max_km',
        hover_name='nombre',
        log_x=True, # Usar escala logarítmica en X para mejor visualización de la distancia
        title=f'Velocidad vs. Distancia de Acercamiento para NEOs ({dias} días)',
        labels={
            'distancia_lunar': 'Distancia de Paso Cercano (Distancias Lunares)',
            'velocidad_km_s': 'Velocidad Relativa (km/s)',
            'es_peligroso_str': 'Peligroso'
        },
        color_discrete_map={'Sí': '#FF4136', 'No': '#007bff'}
    )
    
    fig.update_layout(
       legend_title_text='Potencialmente Peligroso',
       legend=dict(
           orientation="h",
           yanchor="top", # Cambiado de "bottom" a "top"
           y=0.98,
           xanchor="left",
           x=0.01
           ),
           font=dict(
               family="Montserrat", 
               size=12,
               color="black"
               ),
               margin=dict(l=40, r=40, t=70, b=40)
               )
    # --- Devolver Resultados ---
    return [
        formatear_numero(total_neos),
        formatear_numero(peligrosos_count),
        f"{diametro_promedio:.3f} km",
        f"{velocidad_maxima:.2f} km/s",
        fig,
        mensaje_actualizacion,
        df[['nombre', 'diametro_max_km', 'es_peligroso_str', 'distancia_lunar', 'velocidad_km_s', 'fecha_cercana']].to_dict('records')
    ]