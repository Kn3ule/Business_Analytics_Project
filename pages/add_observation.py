import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session, engine, Session

dash.register_page(__name__)

# Funktion zum Laden der neuesten Genus-Optionen
def load_genus_options():
    new_session = Session(bind=engine)
    try:
        genus_options = [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]
    finally:
        # Close the session when done
        new_session.close()
    return genus_options

# Funktion zum Laden der neuesten Location-Optionen
def load_location_options():
    new_session = Session(bind=engine)
    try:
        location_options = [{'label': l.short_title, 'value': l.location_number} for l in session.query(Location).all()]
    finally:
        # Close the session when done
        new_session.close()
    return location_options

#Funktion zum Laden der Animal Optionen
#with new session because of concurrent call
def load_animal_options():
    new_session = Session(bind=engine)
    try:
        animal_options = [{'label': a.visual_features, 'value': a.id} for a in session.query(Animal).all()]
    finally:
        # Close the session when done
        new_session.close()
    return animal_options

layout = html.Div([
    html.H1("Add Observation"),
    dcc.Dropdown(id='filter-dropdown', options=[], placeholder='Select Genus'),
    dcc.Dropdown(id='animal-dropdown', options=[], placeholder='Select Animal'),
    dcc.Dropdown(id='location-dropdown', options=[], placeholder='Select Location'),
    html.Label('Spotted Date Start:'),
    dcc.DatePickerSingle(
        id='spotted-date-start',
        display_format='YYYY-MM-DD',
        placeholder='Select Date'
    ),
    html.Label('Spotted Time Start:'),
    dcc.Input(id='spotted-time-start', type='text', placeholder='HH:MM:SS'),

    html.Label('Spotted Date End:'),
    dcc.DatePickerSingle(
        id='spotted-date-end',
        display_format='YYYY-MM-DD',
        placeholder='Select Date'
    ),
    html.Label('Spotted Time End:'),
    dcc.Input(id='spotted-time-end', type='text', placeholder='HH:MM:SS'),

    html.Button('Add Observation', id='add-observation-button'),
    html.Div(id='observation-output-message')
])

# Callback-Funktion zum Laden der neuesten Genus-Optionen
@callback(Output('filter-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/add-observation':
        return load_genus_options()
    return []

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('location-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_location_options(pathname):
    if pathname == '/add-observation':
        return load_location_options()
    return []

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('animal-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_animal_options(pathname):
    if pathname == '/add-observation':
        return load_animal_options()
    return []


# Callback-Funktion für das Einreichen von Location-Daten
@callback(
    Output('observation-output-message', 'children'),
    [Input('add-observation-button', 'n_clicks')],
    [
        State('filter-dropdown', 'value'),
        State('animal-dropdown', 'value'),
        State('location-dropdown', 'value'),
        State('spotted-date-start', 'date'),  # Hier wurde 'date' hinzugefügt
        State('spotted-time-start', 'value'),
        State('spotted-date-end', 'date'),
        State('spotted-time-end', 'value'),]
)
def add_observation(n_clicks, genus_id, animal_id, location_id, spotted_date_start, spotted_time_start, spotted_date_end, spotted_time_end):
    if n_clicks is not None:

        if spotted_date_start and spotted_time_start:
            spotted_date_start = datetime.strptime(f"{spotted_date_start} {spotted_time_start}", '%Y-%m-%d %H:%M:%S')

        if spotted_date_end and spotted_time_end:
            spotted_date_end = datetime.strptime(f"{spotted_date_end} {spotted_time_end}", '%Y-%m-%d %H:%M:%S')

        if spotted_date_end < spotted_date_start:
            return "Failure: End Time before Start Time"

        animal = session.query(Animal).filter_by(id = animal_id).first()
        location = session.query(Location).filter_by(location_number=location_id).first()
        new_observation = Observation(animal=animal, location=location, start_time=spotted_date_start, end_time=spotted_date_end)
        session.add(new_observation)
        session.commit()
        return "Observation added successfully."
    return None