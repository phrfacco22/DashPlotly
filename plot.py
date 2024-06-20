import plotly.graph_objects as go # or plotly.express as px
from dash import Dash, dcc, html


fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )


app = Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter