import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session, engine, Session
import dash_bootstrap_components as dbc

dash.register_page(__name__)

global genus_options_animal
genus_options_animal = [genus.id for genus in session.query(genus).all()]

#Funktion zum Laden der Animal Optionen
#with new session because of concurrent call
def load_genus_options():
    new_session = Session(bind=engine)
    try:
        genus_options = [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]

    finally:
        # Close the session when done
        new_session.close()
    return genus_options

def load_animal_options(genus_id_selected=None):
    new_session = Session(bind=engine)
    try:
        if genus_id_selected is None:
            animal_options = [{'label': a.visual_features, 'value': a.id} for a in session.query(Animal).all()]
        else:
            animal_options = [{'label': a.visual_features, 'value': a.id} for a in session.query(Animal).filter(Animal.genus_id == genus_id_selected).all()]
    finally:
        # Close the session when done
        new_session.close()
    return animal_options

# Funktion zum Laden der neuesten Location-Optionen
def load_location_options():
    new_session = Session(bind=engine)
    try:
        location_options = [{'label': l.short_title, 'value': l.location_number} for l in session.query(Location).all()]
    finally:
        # Close the session when done
        new_session.close()
    return location_options

layout = html.Div(
style={'backgroundImage': f'url("https://s1.1zoom.me/big0/292/346934-admin.jpg")', 'backgroundSize': 'cover','height': '100vh'},
    children=[
    html.Div(
        [
    html.Div(id="alert-output-add-observation"),
    html.H1("Add Observation", className="display-4 text-center mb-4",style={'font-size': '3em','font-weight': 'bold'}),
    dcc.Dropdown(id='genus-dropdown-observation', options=[], placeholder='Select Genus', className="form-control mb-3"),
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
    dcc.Location(id='url-add-observation')
    ],
        className="container p-5",
        style={'max-width': '600px'}
    )
    ])

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('genus-dropdown-observation', 'options'),
              [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/add-observation':
        return load_genus_options()
    return []

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('animal-dropdown', 'options'),
              [Input('url', 'pathname'),
               Input('genus-dropdown-observation', 'value')])
def update_animal_options(pathname, genus_id):
    if pathname == '/add-observation':
        return load_animal_options(genus_id)
    return []

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('location-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_location_options(pathname):
    if pathname == '/add-observation':
        return load_location_options()
    return []

@callback(Output('animal-dropdown', 'options', allow_duplicate=True),
              [Input('genus-dropdown-observation', 'value')],
          prevent_initial_call=True)
def filter_animal_options(genus_id):
    return load_animal_options(genus_id)


# Callback-Funktion für das Einreichen von Location-Daten
@callback(
    Output('alert-output-add-observation', 'children'),
    Output('url-add-observation', 'href'),
    Output('url-add-observation', 'refresh'),
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
        if animal_id is not None and location_id is not None and spotted_date_start is not None and spotted_time_start is not None and spotted_date_end is not None and spotted_time_end is not None:

            spotted_date_start = datetime.strptime(f"{spotted_date_start} {spotted_time_start}", '%Y-%m-%d %H:%M:%S')
            spotted_date_end = datetime.strptime(f"{spotted_date_end} {spotted_time_end}", '%Y-%m-%d %H:%M:%S')

            if spotted_date_end < spotted_date_start:
                return dbc.Alert(
                    f"End time is before start time!",
                    dismissable=True,
                    color="warning"), '', False

            animal = session.query(Animal).filter_by(id = animal_id).first()
            location = session.query(Location).filter_by(location_number=location_id).first()
            new_observation = Observation(animal=animal, location=location, start_time=spotted_date_start, end_time=spotted_date_end)
            session.add(new_observation)
            session.commit()
            return '', '/', True
        else:
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False