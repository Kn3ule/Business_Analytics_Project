import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Animal, Location, Genus, Observation
from datetime import datetime
from models import my_session as session, engine, Session
import dash_bootstrap_components as dbc

dash.register_page(__name__)


# Load latest genus options
def load_genus_options():
    # New session because of concurrent call
    new_session = Session(bind=engine)
    try:
        genus_options = [{'label': g.species_name, 'value': g.id} for g in session.query(Genus).all()]
    finally:
        # close the session when done
        new_session.close()
    return genus_options


# Load latest animal options and filter animals by selected genus
def load_animal_options(genus_id_selected=None):
    new_session = Session(bind=engine)
    try:
        if genus_id_selected is None:
            # Load all animals
            animal_options = [{'label': a.visual_features, 'value': a.id} for a in new_session.query(Animal).all()]
        else:
            # Only load animals of selected genus
            animal_options = [{'label': a.visual_features, 'value': a.id} for a in
                              new_session.query(Animal).filter(Animal.genus_id == genus_id_selected).all()]
    finally:
        # Close the session when done
        new_session.close()
    return animal_options


# Load latest location options
def load_location_options():
    new_session = Session(bind=engine)
    try:
        location_options = [{'label': l.short_title, 'value': l.location_number} for l in session.query(Location).all()]
    finally:
        # Close the session when done
        new_session.close()
    return location_options


# Read the local image file and encode it to Base64
with open("./images/Raised_Blind.png", "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

layout = html.Div(
    style={'position': 'fixed',
           'top': '10',
           'left': '0',
           'width': '100%',
           'height': '100vh',
           'z-index': '-1',
           'backgroundPosition': 'center',
           'backgroundSize': 'cover',
           'backgroundImage': f'url("data:image/jpeg;base64,{encoded_image}")',
           },
    children=[
        html.Div(
            [
                html.Div(id="alert-output-add-observation"),
                html.H1("Add Observation", className="display-4 text-center mb-4",
                        style={'font-size': '3em', 'font-weight': 'bold'}),
                # Dropdowns for genus, animal, and location
                dcc.Dropdown(id='genus-dropdown-observation', options=[], placeholder='Select Genus',
                             className="form-control mb-3"),
                dcc.Dropdown(id='animal-dropdown', options=[], placeholder='Select Animal',
                             className="form-control mb-3"),
                dcc.Dropdown(id='location-dropdown', options=[], placeholder='Select Location',
                             className="form-control mb-3"),

                # Date picker and input field for start date and time
                dcc.DatePickerSingle(
                    id='spotted-date-start', display_format='YYYY-MM-DD', placeholder='Start Date',
                    className="form-control mb-3",
                ),
                dcc.Input(id='spotted-time-start', type='text', placeholder='Start Time',
                          className="form-control mb-3"),

                # Date picker and input field for end date and time
                dcc.DatePickerSingle(
                    id='spotted-date-end', display_format='YYYY-MM-DD', placeholder='End Date',
                    className="form-control mb-3"
                ),
                dcc.Input(id='spotted-time-end', type='text', placeholder='End Time', className="form-control mb-3"),

                # Button to save the observation
                html.Button('Add Observation', id='add-observation-button', className="btn btn-secondary"),
                dcc.Location(id='url-add-observation')
            ],
            className="container p-5",
            style={'max-width': '600px'}
        )
    ])


# Callback executed when page is loaded
@callback(Output('genus-dropdown-observation', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/add-observation':
        return load_genus_options()
    return []


# Callback executed when page is loaded or genus is selected
@callback(Output('animal-dropdown', 'options'),
          [Input('url', 'pathname'),
           Input('genus-dropdown-observation', 'value')])
def update_animal_options(pathname, genus_id):
    if pathname == '/add-observation':
        return load_animal_options(genus_id)
    return []


# Callback executed when page is loaded
@callback(Output('location-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_location_options(pathname):
    if pathname == '/add-observation':
        return load_location_options()
    return []


# Callback executed when genus is selected
@callback(Output('animal-dropdown', 'options', allow_duplicate=True),
          [Input('genus-dropdown-observation', 'value')],
          prevent_initial_call=True)
def filter_animal_options(genus_id):
    return load_animal_options(genus_id)


# Callback executed when add observation button is clicked
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
        State('spotted-time-end', 'value'), ]
)
def add_observation(n_clicks, animal_id, location_id, spotted_date_start, spotted_time_start, spotted_date_end,
                    spotted_time_end):
    if n_clicks is not None:
        # Check if all values are specified
        if animal_id is not None and location_id is not None and spotted_date_start is not None and spotted_time_start is not None and spotted_date_end is not None and spotted_time_end is not None:

            # Convert date and time to datetime objects
            spotted_date_start = datetime.strptime(f"{spotted_date_start} {spotted_time_start}", '%Y-%m-%d %H:%M:%S')
            spotted_date_end = datetime.strptime(f"{spotted_date_end} {spotted_time_end}", '%Y-%m-%d %H:%M:%S')

            # Show alert if end time is before start time
            if spotted_date_end < spotted_date_start:
                return dbc.Alert(
                    f"End time is before start time!",
                    dismissable=True,
                    color="warning"), '', False

            # Add observation to database
            animal = session.query(Animal).filter_by(id=animal_id).first()
            location = session.query(Location).filter_by(location_number=location_id).first()
            new_observation = Observation(animal=animal, location=location, start_time=spotted_date_start,
                                          end_time=spotted_date_end)
            session.add(new_observation)
            session.commit()
            return '', '/', True
        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False
