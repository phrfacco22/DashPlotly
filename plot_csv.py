import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
 

excel_data = pd.read_excel('csv_plot_valores.xlsx', sheet_name='GRAFICO - VALOR')
excel_data_qtd = pd.read_excel('csv_plot_valores.xlsx', sheet_name='GRAFICO - QUANTIDADE')

df_orgaos = pd.DataFrame(data=excel_data)
df_valores = pd.DataFrame(data=excel_data_qtd)

df_orgaos = df_orgaos.loc[2:25]
df_orgaos['Unnamed: 1'] = pd.to_numeric(df_orgaos['Unnamed: 1'], errors='coerce')
df_orgaos['Unnamed: 2'] = pd.to_numeric(df_orgaos['Unnamed: 2'], errors='coerce')

df_valores = df_valores.loc[1:20]
df_valores['Unnamed: 1'] = pd.to_numeric(df_valores['Unnamed: 1'], errors='coerce')
df_valores['Unnamed: 2'] = pd.to_numeric(df_valores['Unnamed: 2'], errors='coerce')

print(df_valores)

fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Bar(
    x=df_orgaos['Unnamed: 1'],     
    y=df_orgaos['Unnamed: 2'],
    # customdata=df_orgaos['Unnamed: 1', 'Unnamed: 2'].values,
    # text=df_orgaos['Unnamed: 0'],  
    # hovertemplate=
    # '<b>%{text}</b><br>'+
    # '<b>Soma de Saldo Inicial: </b> %{customdata[0]}<br>'+
    # '<b>Soma de Saldo Final: </b> %{customdata[1]}<br>',
    visible=True,
    # name=df_orgaos['Unnamed: 0']
))

fig.update_layout(
    title="Gráfico de Entradas x Saídas",
    xaxis_title="Entradas",
    yaxis_title="Saídas",
    showlegend=True
)

fig.add_trace(go.Bar(
    x=df_valores['Unnamed: 1'],     
    y=df_valores['Unnamed: 2'],
    # customdata=df_orgaos['Unnamed: 1', 'Unnamed: 2'].values,
    # text=df_orgaos['Unnamed: 0'],  
    # hovertemplate=
    # '<b>%{text}</b><br>'+
    # '<b>Soma de Saldo Inicial: </b> %{customdata[0]}<br>'+
    # '<b>Soma de Saldo Final: </b> %{customdata[1]}<br>',
    visible=True,
    # name=df_orgaos['Unnamed: 0']
))

# Add dropdown
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "bar-plot"],
                    label="Valor",
                    method="restyle"
                ),
                dict(
                    args=["type", "bar-plot"],
                    label="Quantidade",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

# Add annotation
fig.update_layout(
    annotations=[
        dict(text="Tipo de Gráfico:", showarrow=False,
        x=0, y=1.085, yref="paper", align="left")
    ]
)


fig.update_layout(
    title="Gráfico de Entradas x Saídas",
    xaxis_title="Entradas",
    yaxis_title="Saídas",
    showlegend=True
)

app = Dash()
 
app.layout = html.Div([
    
     dcc.Tabs([
        dcc.Tab(label='Gráfico Valor', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': df_orgaos['Unnamed: 1'], 'y': df_orgaos['Unnamed: 2'],
                        'type': 'bar'}
                    ]
                }
            )
        ]),
        dcc.Tab(label='Gráfico Quantidade', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': df_valores['Unnamed: 1'], 'y': df_valores['Unnamed: 2'],
                        'type': 'bar'}
                    ]
                }
            )
        ])
    ]),

    # dcc.Graph(id='bar-plot', figure=fig),
    
    html.Label("Filtro de Valor de Entradas (Eixo X)"),
    dcc.RangeSlider(
        id='x-range-slider',
        min=df_orgaos['Unnamed: 1'].min(),
        max=df_orgaos['Unnamed: 1'].max(),
        step=0.1,
        marks=None,
        value=[df_orgaos['Unnamed: 1'].min(), df_orgaos['Unnamed: 1'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    ),
    
    html.Label("Filtro de Valor de Saídas (Eixo Y)"),
    dcc.RangeSlider(
        id='y-range-slider',
        min=df_orgaos['Unnamed: 2'].min(),
        max=df_orgaos['Unnamed: 2'].max(),
        step=0.1,
        marks=None,
        value=[df_orgaos['Unnamed: 2'].min(), df_orgaos['Unnamed: 2'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    )
])

@app.callback(
    
    Output('bar-plot', 'figure'),
    [Input('x-range-slider', 'value'),
    Input('y-range-slider', 'value')]
)
 
def update_graph(x_range, y_range):
    
    traces = []
            
    bar = go.Bar(
        x=df_orgaos['Unnamed: 1'],     
        y=df_orgaos['Unnamed: 2'],
        # customdata=df_orgaos['Unnamed: 1', 'Unnamed: 2'].values,
        # text=df_orgaos['Unnamed: 0'],  
        textposition='auto',
        # hovertemplate=
        # '<b>%{text}</b><br>'+
        # '<b>Soma de Saldo Inicial: </b> %{customdata[0]}<br>'+
        # '<b>Soma de Saldo Final: </b> %{customdata[1]}<br>',
        visible=True,
        # name=
    )
    traces.append(bar)

    bar_qtd = go.Bar(
        x=df_valores['Unnamed: 1'],     
        y=df_valores['Unnamed: 2'],
        # customdata=df_orgaos['Unnamed: 1', 'Unnamed: 2'].values,
        # text=df_orgaos['Unnamed: 0'],  
        textposition='auto',
        # hovertemplate=
        # '<b>%{text}</b><br>'+
        # '<b>Soma de Saldo Inicial: </b> %{customdata[0]}<br>'+
        # '<b>Soma de Saldo Final: </b> %{customdata[1]}<br>',
        visible=True,
        # name=
    )
    traces.append(bar_qtd)
    
    layout = go.Layout(
        title="Gráfico de Entradas x Saídas",
        xaxis_title="Entradas",
        yaxis_title="Saídas",
        showlegend=True
    )
    
    return {'data': traces, 'layout': layout}
     
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
   
