import datetime
from datetime import date
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

from data.data import get_coin_list, get_fiat_list, historical_data, get_info, price_changes
from layout import create_navbar, create_header, create_footer

from app import app

#Main dashboard layout function 
def create_dashboard():
    layout = html.Div([
        create_header(),
        create_navbar(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.CardHeader("Options", className="text-center gx-2"),
                                    html.Div(children="Coin Currency", className="d-flex justify-content-center my-3 font-weight-bold"),
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
                                    html.Div(children="Fiat Currency", className="d-flex justify-content-center my-3 font-weight-bold"),
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
                                    html.Div(children="Date Range", className="d-flex justify-content-center my-3 font-weight-bold"),
                                        dcc.DatePickerRange(
                                        id="datePicker",
                                        min_date_allowed=date(2013, 4, 28),
                                        max_date_allowed=datetime.datetime.now().strftime("%Y-%m-%d"),
                                        start_date=date(2022, 1, 1),
                                        end_date=datetime.datetime.now().strftime("%Y-%m-%d"),
                                        calendar_orientation='vertical',
                                        className="d-flex justify-content-center"
                                        ),
                                ], className="cborder shadow h-100 me-3"
                            ),
                        ], className="col-md-2 gx-0"),
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
                                                                html.Img(id="card-logo", className="img-logo"),
                                                            ], className="col-lg-4 col-sm d-flex align-items-center justify-content-center"
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.Div(id="card-value1", style={"color":"green"}, className="card-title  text-responsive"),
                                                            ], className="col-lg-8 d-flex align-items-center justify-content-center"
                                                        ),
                                                    ],
                                                )
                                            ]
                                        ),
                                    ],className="col-sm me-3 rounded-0"),
                                    dbc.Card([
                                        dbc.CardHeader("Since Last 24H", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P(id="card-value2", className="card-test text-responsive"),
                                            ], className="d-flex align-items-center justify-content-center"
                                        ),
                                    ],className="col-sm me-3 rounded-0"),
                                    dbc.Card([
                                        dbc.CardHeader("Since Last 24H", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P(id="card-value3", className="card-test text-responsive"),
                                            ], className="d-flex align-items-center justify-content-center"
                                        ),
                                    ],className="col-sm me-3 rounded-0"),
                                    dbc.Card([
                                        dbc.CardHeader("Market Cap", className="text-center"),
                                        dbc.CardBody(
                                            [
                                                html.P(id="card-value4", className="card-test text-responsive"),
                                            ], className="d-flex align-items-center justify-content-center"
                                        ),
                                    ],className="col-sm rounded-0"),
                                ], className="gx-0 mb-2"
                            ),
                            dbc.Row(
                                [
                                    html.Div(
                                    children=dcc.Graph(
                                        id="price_plot", config={"displayModeBar": False},className="", style={'width': '100%'})
                                    )
                                ],className="shadow cborder gx-0"
                            )
                        ], className="col-md-10 p-0"
                    ),
                ], className="container-fluid mx-auto mt-2 px-0"
            ),
            dbc.Row(
                children=dcc.Graph(
                    id="candlestick_plot", config={"displayModeBar": True, "scrollZoom": True},
                ),className="container-fluid cborder shadow mx-auto mt-2 gx-0", style={'width': '100%'}
            ),
            create_footer(),
        ], className="min-vh-100 d-flex flex-column"
    )
    return layout

#Charts callback function that check if values in dropdown menu are changed
@app.callback(
    [Output("price_plot", "figure"),Output("candlestick_plot", "figure")],
    Input("fromDropdown", "value"),
    Input("toDropdown", "value"),
    Input("datePicker","start_date"),
    Input("datePicker", "end_date"),
)

#Function to update charts based on values from callback function.
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
            "title": 'Candlestick {} - {}'.format(fromDropdown,toDropdown),
            "hovermode" : "x unified",
            "hoverlabel" : dict(bgcolor='rgba(255,255,255,0.75)',font=dict(color='black')),
            "height" : 700,
            "xaxis" : {
                #"spikesnap" : "cursor",
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

#Cards callbacks based on currency dropdown menu.
@app.callback(
    Output("card-logo","src"),
    Output("card-value1","children"),
    Output("card-value2","children"),
    Output("card-value3","children"),
    Output("card-value4","children"),
    Output('card-value2',"style"),
    Output("card-value3","style"),
    Input("fromDropdown","value"),
    Input("toDropdown","value"),
)

#Function that return all values based on the selected options in dropdown menu 
def update_cards(fromDropdown,toDropdown):
    logo = get_info(fromDropdown)['logo']
    values = price_changes(fromDropdown,toDropdown)
    sign = get_fiat_list(toDropdown)
    cardvalue1 = values['close'].round(decimals=2).iloc[0]
    cardvalue2 = values['price_change'].round(decimals=2).iloc[0]
    cardvalue3 = values['percent_change'].round(decimals=2).iloc[0]
    cardvalue4 = values['high'].round(decimals=2).iloc[0]
    if cardvalue2 > 0:
        cardcolor2 = { 'color':'green' }
    else:
        cardcolor2= { 'color':'red' }

    if cardvalue3 > 0:
        cardcolor3 = { 'color':'green' }
    else:
        cardcolor3 = { 'color':'red' }
    cardvalue1 = str(cardvalue1)+" "+sign
    cardvalue2 = str(cardvalue2)+" "+sign
    cardvalue3 = str(cardvalue3)+" "+(str("%"))
    src = logo.iloc[0]

    return src,cardvalue1,cardvalue2,cardvalue3,cardvalue4, cardcolor2, cardcolor3