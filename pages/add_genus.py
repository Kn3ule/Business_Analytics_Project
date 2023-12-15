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

# Layout der Seite zum Hinzufügen von Genus
layout = html.Div(
style={'backgroundImage': f'url("https://s1.1zoom.me/big0/897/Canada_Winter_Mountains_Rivers_Lake_Scenery_River_558127_1280x959.jpg")', 'backgroundSize': 'cover','height': '100vh',},
    children=[
    html.Div(
        [

    html.H1("Add Genus", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),

    dcc.Input(id='species-name', type='text', placeholder='Species Name', className="form-control mb-3"),
    html.Button('Add Genus', id='add-genus-button', className="btn btn-secondary"),
    html.Div(id='genus-output-message', className="mt-3")
    ],
    className="container p-5",
    style={'max-width': '600px'}
    )
])

# Callback-Funktion für das Einreichen von Genus-Daten
@callback(
    Output('genus-output-message', 'children'),
    [Input('add-genus-button', 'n_clicks')],
    [dash.dependencies.State('species-name', 'value')]
)
def add_genus(n_clicks, species_name):
    if n_clicks is not None:
        new_genus = genus(species_name=species_name)
        session.add(new_genus)
        session.commit()
        return "Genus " + species_name + " added successfully."
    return None