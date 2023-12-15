import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session

dash.register_page(__name__)

# Layout der Seite zum Hinzufügen von Location
layout = html.Div(
style={'backgroundImage': f'url("https://s1.1zoom.me/big0/490/Finland_Parks_Forests_Rivers_Oulanka_National_Park_614746_1280x720.jpg")', 'backgroundSize': 'cover','height': '100vh'},
    children=[
    html.Div(
        [

    html.H1("Add Location", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),

    dcc.Input(id='short-title', type='text', placeholder='Short Title', className="form-control mb-3"),
    dcc.Input(id='description', type='text', placeholder='Description', className="form-control mb-3"),
    html.Button('Add Location', id='add-location-button', className="btn btn-secondary"),
    html.Div(id='location-output-message', className="mt-3")
    ],
    className="container p-5",
    style={'max-width': '600px'}
    )
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
        return "Location " + short_title + " added successfully."
    return None