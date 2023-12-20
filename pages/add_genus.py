import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# add the layout of genus
# add a background picture
layout = html.Div(
style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundImage': f'url("https://s1.1zoom.me/big0/935/418430-blackangel.jpg")', 'backgroundSize': 'cover'},

# create the table to add a genus
    children=[
    html.Div(
        [
    html.Div(id="alert-output-add-genus"),
    html.H1("Add Genus", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),

    dcc.Input(id='species-name', type='text', placeholder='Species Name', className="form-control mb-3"),
    html.Button('Add Genus', id='add-genus-button', className="btn btn-secondary"),
    dcc.Location(id='url-add-genus')
    ],
    className="container p-5",
    style={'max-width': '600px'}
    )
])

# Callback-Funktion für das Einreichen von Genus-Daten
@callback(
    Output('alert-output-add-genus', 'children'),
    Output('url-add-genus', 'href'),
    Output('url-add-genus', 'refresh'),
    [Input('add-genus-button', 'n_clicks')],
    [dash.dependencies.State('species-name', 'value')]
)
def safe_genus(n_clicks, species_name):
    if n_clicks is not None:
        if species_name is not None:
            new_genus = genus(species_name=species_name)
            session.add(new_genus)
            session.commit()
            return '', '/view-genera', True
        else:
            return dbc.Alert(
                f"Please enter the species name!",
                dismissable=True,
                color="warning"), '', False
    return'', '', False