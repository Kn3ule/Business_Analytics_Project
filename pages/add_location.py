import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session

# Layout der Seite zum Hinzufügen von Location
layout = html.Div([
    html.H1("Add Location"),
    dcc.Input(id='short-title', type='text', placeholder='Short Title'),
    dcc.Input(id='description', type='text', placeholder='Description'),
    html.Button('Add Location', id='add-location-button'),
    html.Div(id='location-output-message')
])

# Callback-Funktion für das Einreichen von Location-Daten
@callback(
    Output('location-output-message', 'children'),
    [Input('add-location-button', 'n_clicks')],
    [dash.dependencies.State('short-title', 'value'),
     dash.dependencies.State('description', 'value')]
)
def add_location(n_clicks, short_title, description):
    if n_clicks is not None:
        new_location = Location(short_title=short_title, description=description)
        session.add(new_location)
        session.commit()
        return "Location added successfully."
    return None