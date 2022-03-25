import dash
from dash import dcc
from dash import html
import numpy as np
import pandas as pd

from .data import get_data_test
from .layout import html_layout


def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/',
    )

    df = get_data_test('BTC','USD')
    dash_app.index_string = html_layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(
                id="test_data",
                figure={
                    "data": [
                        {
                            "x": df["timestamp"],
                            "y": df["close"],
                            "mode": "lines",
                            'marker': {'color': ["#E12D39"]},
                            'name': df["close"],
                        }
                    ],
                    "layout": {
                        "title": "BTC - USD",
                        "xaxis": {"fixedrange": True},
                        "yaxis": {"fixedrange": True},
                        "colorway": ["#E12D39"],
                        "height": 500,
                        "padding": 150,
                        "hovermode": "x unified",
                    },
                },
            ),
        ],
        id="dash-container",
    )
    return dash_app.server
