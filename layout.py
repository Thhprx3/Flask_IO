from dash import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc

#Function to create header that is called from each page to avoid code duplication
def create_header():

    header = html.Header(
        [
            html.Center([
                html.H1("Crypto-Scums")]
            )]
    )
    return header

#Function to create navbar that is called from each page to avoid code duplication
def create_navbar():
    navbar = html.Nav(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Dashboard", active="exact", href="/")),
                    dbc.NavItem(dbc.NavLink("Prediction", active="exact", href="/prediction")),
                ],
                #pills=True,
                justified=True,
                className="nav-border shadow",
            ),
        ],
    )
    return navbar

#Function to create footer that is called from each page to avoid code duplication
def create_footer():
    footer = html.Footer(
        [
            html.Center(children=[
                html.H5([
                    html.A("Github", className="text-white text-decoration-none", href="https://github.com/Thhprx3/Flask_IO"),
                ])
            ]),
        ], className="footer-style shadow"
    )
    return footer