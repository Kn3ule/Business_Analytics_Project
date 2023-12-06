import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session

# Layout der Seite zum Hinzufügen von Genus
layout = html.Div([
    html.H1("Add Genus"),
    dcc.Input(id='species-name', type='text', placeholder='Species Name'),
    html.Button('Add Genus', id='add-genus-button'),
    html.Div(id='genus-output-message')
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
        return "Genus added successfully."
    return None

# For each page, register the layout and callback
dash.register_page(__name__, layout=layout, callback=add_genus)