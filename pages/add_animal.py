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

layout = html.Div(
    style={'backgroundImage': f'url("https://s1.1zoom.me/big0/479/Rivers_Forests_Mountains_American_bison_Grass_516890_1280x821.jpg")', 'backgroundSize': 'cover','height': '100vh'},
    children=[
        html.Div(
        [
            html.H1("Add animal", className="display-4 text-center mb-4", style={'font-size': '3em','font-weight': 'bold'}),

            dcc.Dropdown(id='genus-dropdown', options=[], placeholder='Select Genus', className="form-control mb-3"),
            dcc.Dropdown(id='gender-dropdown', options=["Male", "Female", "Diverse"], placeholder='Select Gender',
                         className="form-control mb-3"),

            dcc.Input(id='visual-features', type='text', placeholder='Visual Features', className="form-control mb-3"),
            dcc.Input(id='estimated-age', type='number', placeholder='Estimated Age (years)', className="form-control mb-3"),
            dcc.Input(id='estimated-weight', type='number', placeholder='Estimated Weight (kg)', className="form-control mb-3"),
            dcc.Input(id='estimated-size', type='number', placeholder='Estimated Size (cm)', className="form-control mb-3"),

            html.Button('Submit', id='submit-animal-button', className="btn btn-secondary"),
            html.Div(id='animal-output-message', className="mt-3"),
        ],
        className="container p-5",
        style={'max-width': '600px'}
    )
])


# Callback-Funktion zum Laden der neuesten Genus-Optionen
@callback(Output('genus-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/add-animal':
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