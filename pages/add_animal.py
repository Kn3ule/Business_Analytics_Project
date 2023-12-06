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

# Funktion zum Laden der neuesten Genus-Optionen
def load_genus_options():
    return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]


# Layout der Seite zum Hinzufügen von Tierdaten
layout = html.Div([
    html.H1("Add Animal Data"),
    dcc.Dropdown(id='genus-dropdown', options=[], placeholder='Select Genus'),
    dcc.Dropdown(id='gender-dropdown', options=["male", "female", "diverse"], placeholder='Select Gender'),
    dcc.Input(id='visual-features', type='text', placeholder='Visual Features'),
    dcc.Input(id='estimated-age', type='number', placeholder='Estimated Age'),
    dcc.Input(id='estimated-weight', type='number', placeholder='Estimated Weight'),
    dcc.Input(id='estimated-size', type='number', placeholder='Estimated Size'),

    
    html.Button('Submit', id='submit-animal-button'),
    html.Div(id='animal-output-message')
])

# Callback-Funktion zum Laden der neuesten Genus-Optionen
@callback(Output('genus-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/':
        return load_genus_options()
    return []



# Callback-Funktion zum Speichern von Tierdaten
@callback(
    Output('animal-output-message', 'children'),
    [Input('submit-animal-button', 'n_clicks')],
    [
        State('genus-dropdown', 'value'),
        State('gender-dropdown', 'value'),
        State('visual-features', 'value'),
        State('estimated-age', 'value'),
        State('estimated-weight', 'value'),
        State('estimated-size', 'value'),
    ]
)
def save_animal(n_clicks, genus_id, gender, visual_features, estimated_age, estimated_weight, estimated_size):
    if n_clicks is None:
        return None
    
    try:

        animal = Animal(
            genus_id=genus_id,
            gender=gender,
            visual_features= visual_features,
            estimated_age=estimated_age,
            estimated_weight=estimated_weight,
            estimated_size=estimated_size
        )
        session.add(animal)
        session.commit()


        return f"Tier wurde erfolgreich hinzugefügt! ID: {animal.id}"

    except Exception as e:
        return f"Fehler beim Hinzufügen des Tiers: {e}"