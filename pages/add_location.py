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

# Layout der Seite zum Hinzufügen von Location
layout = html.Div(
style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundImage': f'url("https://s1.1zoom.me/big0/490/Finland_Parks_Forests_Rivers_Oulanka_National_Park_614746_1280x720.jpg")', 'backgroundSize': 'cover'},
    children=[
    html.Div(
        [
    html.Div(id="alert-output-add-location"),
    html.H1("Add Location", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),

    dcc.Input(id='short-title', type='text', placeholder='Short Title', className="form-control mb-3"),
    dcc.Input(id='description', type='text', placeholder='Description', className="form-control mb-3"),
    html.Button('Add Location', id='add-location-button', className="btn btn-secondary"),
    dcc.Location(id='url-add-location')
    ],
    className="container p-5",
    style={'max-width': '600px'}
    )
    ])

# Callback-Funktion für das Einreichen von Location-Daten
@callback(
    Output('alert-output-add-location', 'children'),
    Output('url-add-location', 'href'),
    Output('url-add-location', 'refresh'),
    [Input('add-location-button', 'n_clicks')],
    [dash.dependencies.State('short-title', 'value'),
     dash.dependencies.State('description', 'value')]
)
def add_location(n_clicks, short_title, description):
    if n_clicks is not None:
        if short_title is not None and description is not None:
            new_location = Location(short_title=short_title, description=description)
            session.add(new_location)
            session.commit()
            return '', '/view-locations', True

        else:
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False