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

layout = html.Div(
style={'backgroundImage': f'url("https://s1.1zoom.me/big0/292/346934-admin.jpg")', 'backgroundSize': 'cover','height': '100vh'},
    children=[
    html.Div(
        [

    html.H1("Add Observation", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),
    dcc.Dropdown(id='animal-dropdown', options=[], placeholder='Select Animal', className="form-control mb-3"),
    dcc.Dropdown(id='location-dropdown', options=[], placeholder='Select Location', className="form-control mb-3"),

    dcc.DatePickerSingle(
        id='spotted-date-start', display_format='YYYY-MM-DD', placeholder='Start Date', className="form-control mb-3",
    ),

    dcc.Input(id='spotted-time-start', type='text', placeholder='Start Time', className="form-control mb-3"),

    dcc.DatePickerSingle(
    id='spotted-date-end', display_format='YYYY-MM-DD', placeholder='End Date', className="form-control mb-3"
    ),

    dcc.Input(id='spotted-time-end', type='text', placeholder='End Time', className="form-control mb-3"),

    html.Button('Add Observation', id='add-observation-button', className="btn btn-secondary"),
    html.Div(id='observation-output-message')
    ],
        className="container p-5",
        style={'max-width': '600px'}
    )
    ])

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
        State('animal-dropdown', 'value'),
        State('location-dropdown', 'value'),
        State('spotted-date-start', 'date'),  # Hier wurde 'date' hinzugefügt
        State('spotted-time-start', 'value'),
        State('spotted-date-end', 'date'),
        State('spotted-time-end', 'value'),]
)
def add_observation(n_clicks, animal_id, location_id, spotted_date_start, spotted_time_start, spotted_date_end, spotted_time_end):
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