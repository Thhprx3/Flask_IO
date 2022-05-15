from datetime import datetime
import os
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

from app import app

from data.data import historical_data
from layout import create_navbar, create_header, create_footer
from pred import prepare_data, split, model_data, fit_model, predict_values, plot_data, predict


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
                                            html.Div(
                                                [
                                                    html.Div(children="Neurons", className="display-4 m-auto font-weight-bold"),
                                                    dcc.Dropdown(
                                                        id='dropdownNeurons',
                                                        options=[
                                                            {'label': value, 'value': value}
                                                            for value in range(5,255,5)
                                                        ],
                                                        value=5,
                                                        clearable=False,
                                                        searchable=False,
                                                        className="mx-auto my-5 d-flex"
                                                    ),
                                                    html.Div(children="Steps", className="display-4 m-auto font-weight-bold"),
                                                    dcc.Dropdown(
                                                        id='dropdownSteps',
                                                        options=[
                                                            {'label': value, 'value': value}
                                                            for value in range(5,105,5)
                                                        ],
                                                        value=5,
                                                        clearable=False,
                                                        searchable=False,
                                                        className="mx-auto my-5 d-flex"
                                                    ),
                                                    html.Button("START",
                                                        id="apply-button",
                                                        n_clicks=0,
                                                        className="btn btn-secondary btn-lg float-end m-auto "
                                                    ),
                                                ], className="d-flex justify-content-center"
                                            ),
                                        ], className="cborder shadow h-100 me-1"
                                    )
                                ], className="col-md-9 gx-0"
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            dbc.CardHeader("Total steps:", className="text-center"),
                                            html.Div(id="steps-value", className="display-1 font-weight-bold d-flex justify-content-center my-3"),
                                            dcc.Interval(
                                                id='interval-steps',
                                                interval=1*1000,
                                                n_intervals=0,
                                            )
                                        ], className="cborder shadow h-100 ms-1"
                                    )

                                ], className="col-md-3 gx-0 g-0"
                            ),
                        ], className="mt-2 gx-0"
                    ),
                    dbc.Row(
                        [
                            dcc.Graph(id='model_plot', className="", style={'width': '100%'}),
                        ],className="shadow cborder gx-0 mt-2"
                    ),
                    dbc.Row(
                        [
                            dbc.Card([
                                dbc.CardHeader("TrainScore", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="train-score", className="card-test text-responsive"),
                                    ], className="d-flex align-items-center justify-content-center"
                                ),
                            ],className="col-sm me-3 rounded-0"),
                            dbc.Card([
                                dbc.CardHeader("TestScore", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="test-score", className="card-test text-responsive"),
                                    ], className="d-flex align-items-center justify-content-center"
                                ),
                            ],className="col-sm me-3 rounded-0"),
                            dbc.Card([
                                dbc.CardHeader("T+1", className="text-center"),
                                dbc.CardBody(
                                    [
                                        html.P(id="forecast-value", className="card-test text-responsive"),
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

@app.callback(
    Output('steps-value', 'children'),
    [Input('interval-steps', 'n_intervals')]
)

def get_run_log(n):
    names = ['step', 'loss', 'mae', 'val_loss', 'val_mae']

    logger = pd.read_csv('run.csv', names=names)
    if os.path.getsize('run.csv') != 0:
        json = logger.to_json(orient='split')
        if json:
            logger_df = pd.read_json(json, orient='split')
            step = int(logger_df['step'].iloc[-1])
            return step+1
    else:
        return 0

@app.callback(
    Output('model_plot', 'figure'),
    Output('train-score','children'),
    Output('test-score','children'),
    Output('forecast-value','children'),
    Input('apply-button', 'n_clicks'),
    State("dropdownNeurons","value"),
    State("dropdownSteps","value"),
)
def button_run(n_clicks, dropdownNeurons, dropdownSteps):
    

    if not n_clicks:
        raise PreventUpdate
        
    now = datetime.now().strftime('%Y-%m-%d')

    with open("run.csv", "w"):
        data = historical_data('USD','BTC','2013-01-01',now)
        close_dataset = prepare_data(data)
        train,test = split(close_dataset)
        Xtrain, Ytrain, Xtest, Ytest = model_data(train,test)
        model = fit_model(Xtrain, Ytrain, Xtest, Ytest, dropdownNeurons,dropdownSteps)
        TrainPrediction, Ytrain, TestPrediction, Ytest, TrainScore, TestScore = predict_values(model, Xtrain, Ytrain, Xtest, Ytest, close_dataset)
        inverted_dataset, trainPredictPlot, testPredictPlot = plot_data(close_dataset, TrainPrediction, TestPrediction)
        
        num_prediction = 1
        Forecast = predict(num_prediction, model, close_dataset)

        dataset_df = pd.DataFrame(inverted_dataset, columns=['values'])
        train_df = pd.DataFrame(trainPredictPlot , columns=['values'])
        test_df = pd.DataFrame(testPredictPlot , columns=['values'])
        
        figure = go.Figure()

        figure.add_trace(
            go.Scatter(
                y=dataset_df['values'],
                mode="lines",
                name="Real Data",
                line=dict(
                    color="blue"
                )
            )
        )
        figure.add_trace(
            go.Scatter(
                y=train_df['values'],
                mode="lines",
                name="Train Data",
                line=dict(
                    color="red"
                )
            )
        )
        figure.add_trace(
            go.Scatter(
                y=test_df['values'],
                mode="lines",
                name="Test Data",
                line=dict(
                    color="green"
                )
            )
        )
        figure.update_layout(hovermode="x unified")

    Forecast = round(Forecast, 2)
    TrainScore = round(TrainScore, 2)
    TestScore = round(TestScore, 2)

    return figure, TrainScore, TestScore, Forecast



