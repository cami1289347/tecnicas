import dash
from dash import html


dash.register_page(__name__,path="/",name="Inicio",
)


layout = html.Main([
    html.Section([
        html.Div([
            html.H1([
                "Bienvenidos a ",
                html.Strong("Tecnicas de Modelamiento!", className="titulo-destaque")
            ], className="presentacion__contenido__titulo"),

            html.P("""
                ¡Hola! Soy Lucia Moran, estudiante de la carrera de Computación Científica
                en la Universidad Nacional Mayor de San Marcos. En este sitio estaré escribiendo un poco 
                sobre mis clases de tecnicas de modelamiento.
            """, className="presentacion__contenido__texto"),

        

        ], className="presentacion__contenido"),

        html.Img(
            src="/assets/imagenes/2.png",
            alt="Foto de Lucia Moran desarrollando un proyecto",
            className="presentacion__imagen"
        )
    ], className="presentacion"),

    html.Footer([
        html.P("Desarrollado por Lucia Moran")
    ], className="footer")
])
