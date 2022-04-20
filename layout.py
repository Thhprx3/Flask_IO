from dash import Input, Output
from dash import dcc, html
import dash_bootstrap_components as dbc

def create_header():

    header = html.Header(
        [
            html.Center([
                html.H1("Crypto-Scums")]
            )]
    )
    return header

def create_navbar():
    navbar = html.Nav(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Dashboard", active="exact", href="/"), className="nav-border-left"),
                    dbc.NavItem(dbc.NavLink("Prediction", active="exact", href="/prediction"), className="nav-border-right"),
                ],
                #pills=True,
                justified=True,
                className="nav-border shadow",
            ),
        ],
    )
    return navbar

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