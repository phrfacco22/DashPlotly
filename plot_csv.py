import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
 

x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
y_bar = [10, 15, 7, 10, 17, 15, 14, 20, 16, 19, 15, 17]
y_area = [12, 13, 10, 14, 15, 13, 16, 18, 15, 17, 14, 16]

df_orgaos = pd.DataFrame(data=dict(x=y_bar, y=y_area))
 
fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Bar(
    x=y_area,     
    y=y_bar,
    # customdata=
    text=x,  
    textposition='auto',
    marker=dict(opacity=0.7),
    hovertemplate=
    '<b>%{text}</b>'+
    '<b>%</b>',
    visible=True
))

fig.update_layout(
    title="Gráfico",
    xaxis_title="",
    yaxis_title="",
    showlegend=True
)

app = Dash()
 
app.layout = html.Div([
    
    
    dcc.Graph(id='scatter-plot', figure=fig),
    
    html.Label("Filtro de  (Eixo X)"),
    dcc.RangeSlider(
    id='x-range-slider',
    min=df_orgaos.min(),
    max=df_orgaos.max(),
    step=0.1,
    marks=None,
    value=[df_orgaos.min(), df_orgaos.max()],
    tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    ),
    
    html.Label("Filtro de  (Eixo Y)"),
    dcc.RangeSlider(
    id='y-range-slider',
    min=df_orgaos.min(),
    max=df_orgaos.max(),
    step=0.1,
    marks=None,
    value=[df_orgaos.min(), df_orgaos.max()],
    tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    )
])

@app.callback(
    
    Output('scatter-plot', 'figure'),
    [Input('x-range-slider', 'value'),
    Input('y-range-slider', 'value')]
)
 
def update_graph(x_range, y_range):
    
    traces = []
            
    scatter = go.Bar(
        x=y_area,     
        y=y_bar,
        # customdata=
        text=x,  
        textposition='auto',
        marker=dict(opacity=0.7),
        hovertemplate=
        '<b>%{text}</b>'+
        '<b>%</b>',
        visible=True,
    )
    traces.append(scatter)
    
    layout = go.Layout(
        title="Gráfico de Barras",
        xaxis_title="",
        yaxis_title="",
        showlegend=True
    )
    
    return {'data': traces, 'layout': layout}
     
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
   
