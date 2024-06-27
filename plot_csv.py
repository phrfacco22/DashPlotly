import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots


excel_data = pd.read_excel('csv_plot_valores.xlsx', sheet_name='GRAFICO - VALOR')
excel_data_qtd = pd.read_excel('csv_plot_valores.xlsx', sheet_name='GRAFICO - QUANTIDADE')

secretarias_df = pd.DataFrame(data=excel_data)
df_qtd = pd.DataFrame(data=excel_data_qtd)

secretarias_df = secretarias_df.loc[2:25]
secretarias_df['Unnamed: 1'] = pd.to_numeric(secretarias_df['Unnamed: 1'], errors='coerce')
secretarias_df['Unnamed: 2'] = pd.to_numeric(secretarias_df['Unnamed: 2'], errors='coerce')

df_qtd = df_qtd.loc[1:20]
df_qtd['Unnamed: 1'] = pd.to_numeric(df_qtd['Unnamed: 1'], errors='coerce')
df_qtd['Unnamed: 2'] = pd.to_numeric(df_qtd['Unnamed: 2'], errors='coerce')

df_merge = secretarias_df.join(df_qtd, lsuffix='Unnamed: 0', rsuffix='Unnamed: 0')

fig = make_subplots(rows=1, cols=1)

fig.add_trace(go.Bar(
    x=secretarias_df['Unnamed: 1'],
    y=secretarias_df['Unnamed: 2'],
    text='Valores',
    hovertemplate=
    '<b>Valor de Entradas: </b> %{x}<br>'+
    '<b>Valor de Saídas: </b> %{y}<br>',
    visible=True,
    name='Valores'
))

fig.add_trace(go.Bar(
    x=df_qtd['Unnamed: 1'],
    y=df_qtd['Unnamed: 2'],
    text='Valores',
    hovertemplate=
    '<b>Quantidade de Entrada: </b> %{x}<br>'+
    '<b>Quantidade de Saída : </b> %{y}<br>',
    visible=True,
    name='Quantidades'
))

fig.update_layout(
    title="Gráfico de Entradas X Saídas (Valor/Quantidade)",
    xaxis_title="Entradas",
    yaxis_title="Saídas",
    showlegend=True
)

app = Dash()

app.layout = html.Div([


    dcc.Graph(id='bar-plot', figure=fig),

    html.Label("Filtro de Valor de Entradas (Eixo X)"),
    dcc.RangeSlider(
        id='x-range-slider',
        min=secretarias_df['Unnamed: 1'].min(),
        max=secretarias_df['Unnamed: 1'].max(),
        step=0.1,
        marks=None,
        value=[secretarias_df['Unnamed: 1'].min(), secretarias_df['Unnamed: 1'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    ),

    html.Label("Filtro de Valor de Saídas (Eixo Y)"),
    dcc.RangeSlider(
        id='y-range-slider',
        min=secretarias_df['Unnamed: 2'].min(),
        max=secretarias_df['Unnamed: 2'].max(),
        step=0.1,
        marks=None,
        value=[secretarias_df['Unnamed: 2'].min(), secretarias_df['Unnamed: 2'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    ),
    html.Label("Filtro de Quantidade de Entradas (Eixo X)"),
    dcc.RangeSlider(
        id='x-range-slider-qtd',
        min=df_qtd['Unnamed: 1'].min(),
        max=df_qtd['Unnamed: 1'].max(),
        step=0.1,
        marks=None,
        value=[df_qtd['Unnamed: 1'].min(), df_qtd['Unnamed: 1'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    ),

    html.Label("Filtro de Quantidade de Saídas (Eixo Y)"),
    dcc.RangeSlider(
        id='y-range-slider-qtd',
        min=df_qtd['Unnamed: 2'].min(),
        max=df_qtd['Unnamed: 2'].max(),
        step=0.1,
        marks=None,
        value=[df_qtd['Unnamed: 2'].min(), df_qtd['Unnamed: 2'].max()],
        tooltip={"placement": "bottom", "always_visible": False, "style": {"color": "LightSteelBlue", "fontSize": "10px"}}
    )
])

@app.callback(

    Output('bar-plot', 'figure'),
    [Input('x-range-slider', 'value'),
    Input('x-range-slider-qtd', 'value'),
    Input('y-range-slider-qtd', 'value'),
    Input('y-range-slider', 'value')]
)

def update_graph(x_range, y_range, x_range_qtd, y_range_qtd):

    filtered_df = secretarias_df[
        (secretarias_df["Unnamed: 1"] >= x_range[0]) & (secretarias_df['Unnamed: 1'] <= x_range[1]) &
        (secretarias_df["Unnamed: 2"] >= y_range[0]) & (secretarias_df['Unnamed: 2'] <= y_range[1])
    ]

    filtered_df_qtd = df_qtd[
        (df_qtd["Unnamed: 1"] >= x_range_qtd[0]) & (df_qtd['Unnamed: 1'] <= x_range_qtd[1]) &
        (df_qtd["Unnamed: 2"] >= y_range_qtd[0]) & (df_qtd['Unnamed: 2'] <= y_range_qtd[1])
    ]

    traces = []

    bar = go.Bar(
        x=filtered_df['Unnamed: 1'],
        y=filtered_df['Unnamed: 2'],
        hovertemplate=
        '<b>Valor de Entradas: </b> %{x}<br>'+
        '<b>Valor de Saídas: </b> %{y}<br>',
        visible=True,
        name='Valores'
    )
    traces.append(bar)

    bar_qtd = go.Bar(
        x=filtered_df_qtd['Unnamed: 1'],
        y=filtered_df_qtd['Unnamed: 2'],
        hovertemplate=
        '<b>Quantidade de Entrada: </b> %{x}<br>'+
        '<b>Quantidade de Saída : </b> %{y}<br>',
        visible=True,
        name='Quantidades'
    )
    traces.append(bar_qtd)

    layout = go.Layout(
        title="Gráfico de Entradas X Saídas (Valor/Quantidade)",
        xaxis_title="Entradas",
        yaxis_title="Saídas",
        showlegend=True
    )

    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

