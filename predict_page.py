from dash import html
from layout import create_navbar, create_header, create_footer
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_predict():
    layout = html.Div([
        create_header(),
        create_navbar(),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            dbc.CardHeader("Model settings", className="text-center"),
                                            html.Div(children="Steps", className="d-flex justify-content-center my-3 font-weight-bold"),
                                            html.Div(children="Layers", className="d-flex justify-content-center my-3 font-weight-bold"),
                                        ], className="cborder shadow h-100 me-1"
                                    )
                                ], className="col-md-9 gx-0 g-0"
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            dbc.CardHeader("Total steps:", className="text-center"),
                                            html.Div(children="Total Steps", className="d-flex justify-content-center my-3 font-weight-bold"),
                                        ], className="cborder shadow h-100 ms-1"
                                    )

                                ], className="col-md-3 gx-0 g-0"
                            ),
                        ], className="mt-2"
                    ),
                    dbc.Row(
                        [
                            html.Div(
                            children=dcc.Graph(
                                id="model_chart", config={"displayModeBar": False}, className="", style={'width': '100%'})
                            ),
                        ],className="shadow cborder gx-0 mt-2"
                    ),
                    dbc.Row(
                        [
                            html.Div(
                            children=dcc.Graph(
                                id="forecast_chart", config={"displayModeBar": False}, className="", style={'width': '100%'})
                            ),
                        ],className="shadow cborder gx-0 mt-2"
                    ),
                    dbc.Row(
                        [
                            dbc.Card([
                                dbc.CardHeader("T+1", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="card-value2", className="card-test text-responsive"),
                                    ], className="d-flex align-items-center justify-content-center"
                                ),
                            ],className="col-sm me-3 rounded-0"),
                            dbc.Card([
                                dbc.CardHeader("T+2", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="card-value3", className="card-test text-responsive"),
                                    ], className="d-flex align-items-center justify-content-center"
                                ),
                            ],className="col-sm me-3 rounded-0"),
                            dbc.Card([
                                dbc.CardHeader("T+3", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="card-value4", className="card-test text-responsive"),
                                    ], className="d-flex align-items-center justify-content-center"
                                ),
                            ],className="col-sm rounded-0"),
                        ], className="gx-0 mt-2"
                    ),
                ], className="container-fluid px-0 min-vh-100"
            ),
            create_footer(),
        ], className="min-vh-100 d-flex flex-column"
    )
    return layout