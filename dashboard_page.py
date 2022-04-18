import datetime
from datetime import date
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from data.data import get_coin_list, get_first_date, get_fiat_list, historical_data, get_info
from layout import create_navbar, create_header, create_footer

from app import app

def create_dashboard():
    layout = html.Div([
        create_header(),
        create_navbar(),
        create_footer(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(children="Symbol", className="d-flex justify-content-center align-items-center"),
                                dcc.Dropdown(
                                    id="fromDropdown",
                                    options=[
                                        {"label": symbol, "value": symbol}
                                        for symbol in get_coin_list()['symbol']
                                    ],
                                    value="BTC",
                                    clearable=True,
                                    className="dropdown d-flex justify-content-center",
                                ),
                            html.Div(children="Symbol2", className="d-flex justify-content-center"),
                                dcc.Dropdown(
                                    id="toDropdown",
                                    options=[
                                        {"label" : symbol, "value" : symbol}
                                        for symbol in get_fiat_list()['symbol']
                                    ],
                                    value="USD",
                                    clearable=True,
                                    className="dropdown d-flex justify-content-center",
                                ),
                            html.Div(children="Date", className="d-flex justify-content-center"),
                                dcc.DatePickerRange(
                                  id="datePicker",
                                  min_date_allowed=date(2013, 4, 28),
                                  max_date_allowed=datetime.datetime.now().strftime("%Y-%m-%d"),
                                  start_date=date(2022, 1, 1),
                                  end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                                  calendar_orientation='vertical',
                                  className="d-flex justify-content-center"
                                ),
                        ], className="col-md-3 content-border shadow rounded"),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Card([
                                        dbc.CardHeader("Current Price", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dbc.CardImg(
                                                                    className="img-fluid rounded-start img-thumbnail"
                                                                ),                                                      
                                                            ], className="col-md-4"
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.P("value", className="card-test"),
                                                            ], className="col-md-8"
                                                        )
                                                    ], className="flex-fill"
                                                )
                                            ]
                                        ),
                                    ],className="col-sm m-2 "),
                                    dbc.Card([
                                        dbc.CardHeader("Total Sell", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P("value", className="card-test"),
                                            ]
                                        ),
                                    ],className="col-sm m-2"),
                                    dbc.Card([
                                        dbc.CardHeader("Total Buy", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P("value", className="card-test"),
                                            ]
                                        ),
                                    ],className="col-sm m-2"),
                                    dbc.Card([
                                        dbc.CardHeader("Market Cap", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P("value", className="card-test"),
                                            ]
                                        ),
                                    ],className="col-sm m-2"),
                                ], className="gx-0 content-border shadow rounded"
                            ),
                            dbc.Row(
                                children=dcc.Graph(
                                    id="price_plot", config={"displayModeBar": False},
                                ),className="content-border shadow rounded p-2"
                            ),
                        ]
                    ),
                ], className="container-fluid content-border shadow rounded m-2"
            ),
            dbc.Row(
                children=dcc.Graph(
                    id="candlestick_plot", config={"displayModeBar": True, "scrollZoom": True, },
                ),className="container-fluid content-border shadow rounded p-2 gx-0"
            ),
        ], className='min-vh-100 d-flex flex-column'
    )
    return layout

@app.callback(
    [Output("price_plot", "figure"),Output("candlestick_plot", "figure")],
    Input("fromDropdown", "value"),
    Input("toDropdown", "value"),
    Input("datePicker","start_date"),
    Input("datePicker", "end_date"),
)

def update_charts(fromDropdown, toDropdown, start_date, end_date):

    df = historical_data(toDropdown,fromDropdown,str(start_date),str(end_date))
    
    mask = (
        (df.symbol == fromDropdown)
        & (df.timestamp >= start_date)
        & (df.timestamp <= end_date)
    )
    mask_data = df.loc[mask, :]
    price = {
        "data": [
            {
                "x": mask_data["timestamp"],
                "y": df["close"],
                "type": "line",
                "spikedash" : "solid",
                "line" : { "shape" : "spline", "width" : "3"},
            }
        ],
        "layout": {
            "title": '{} - {}'.format(fromDropdown,toDropdown),
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "hovermode": "x unified",
            "hoverlabel" : dict(bgcolor='rgba(255,255,255,0.75)',font=dict(color='black')),
            "xaxis" : {
                "showexponent" : "all",
                "spikedash" : "dash",
                "spikethickness" : "1",
                "spikesnap" : "cursor",
                "spikemode" : "across"
            },
        },
    }
    candlestick = {
        "data" : [
            {
                "x" : mask_data["timestamp"],
                "open" : df["open"],
                "high" : df["high"],
                "low" : df["low"],
                "close" : df["close"],
                "type" : "candlestick",
                "marker" : { "size" : 12, },
            }
        ],
        "layout" : {
            "hovermode" : "x unified",
            "hoverlabel" : dict(bgcolor='rgba(255,255,255,0.75)',font=dict(color='black')),
            "height" : 700,
            "xaxis" : {
                "spikesnap" : "cursor",
                "spikedash": "longdashdot",
                "spikethickness": 1,
                "spikecolor": "rgb(0,176,246)",
                "rangeslider" : {"visible":False},
            },
            'plot_bgcolor' : 'white',
            'font' : {'color' : 'black'},
            "yaxis" : {
                "gridwidth" : 4,
                "fixedrange": True,
            },
        }
    }
    return price, candlestick