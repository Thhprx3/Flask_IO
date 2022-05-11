import dash
import dash_bootstrap_components as dbc

#Include BOOTSTRAP css, so we can access it later in styling our pages
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

#Define app to be run as server
server = app.server
app.title = "Definately not Dash"