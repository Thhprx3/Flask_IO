from dash import html
from layout import create_navbar, create_header, create_footer

def create_predict():
    layout = html.Div([
        create_header(),
        create_navbar(),
        create_footer(),
        html.H1([""])
    ])
    return layout