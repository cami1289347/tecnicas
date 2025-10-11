def fucion_graficas_ecu_log():
    t=np.linspace(0, t_max, 20)

    P=(P0*K*np.exp(r*t))/((K-P0)+P0*np.exp(r*t))

    trace_poblacion=go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        name='Población P(t)',
        line=dict(
            color='blue',
            width=2
        ),
        marker=dict(
            size=6,
            color='black',
            symbol='circle'
        ),
        hovertemplate='t: %{x:.2f}<br>P(t): %{y: .2f}<extra></extra>'
    )
    trace_capacidad= go.Scatter(
        x=[0, t_max],
        y=[K,K],
        mode='lines',
        name='capcidad de carga (K)',
        line=dict(
            color='red',
            width=2,
            dash='dot'
        ),
         hovertemplate='K: %{y:.2f}<extra></extra>'
    )

    fig=go.Figure(data=[trace_poblacion, trace_capacidad])
    
    fig.update_layout(
    title=dict(
        text='<b>Modelo logístico de crecimiento poblacional</b>',
        font=dict(size=20, color='black'),
        x=0.5,
        y=0.95
    ),
    xaxis_title='Tiempo (t)',
    yaxis_title='Población P(t)',
    margin=dict(l=40, r=40, t=70, b=40),
    paper_bgcolor='lightblue',
    plot_bgcolor='white',
    font=dict(
        family='Outfit', 
        size=11, 
        color='black'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        ) 
    )
    
    fig.update_xaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range=[0, t_max]
    )

    fig.update_yaxes(
    showgrid=True, gridwidth=1, gridcolor='lightpink',
    zeroline=True, zerolinewidth=2, zerolinecolor='red',
    showline=True, linecolor='black', linewidth=2, mirror=True,
    range=[0, K+K*0.1]
    )
    return fig