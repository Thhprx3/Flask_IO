from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from dashboard_page import create_dashboard
from predict_page import create_predict

from app import app

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/prediction':
        return create_predict()
    else:
        return create_dashboard()


if __name__ == '__main__':
    app.run_server(debug=False)