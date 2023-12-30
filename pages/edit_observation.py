import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from models import Animal, Genus, Location, Observation, Session, engine
from models import my_session as session
from datetime import datetime

dash.register_page(__name__, path_template='/edit-observation/<id>')

global observation_id
global observation_data


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


# Read the local image file and encode it to Base64
with open("./images/Forests_Stones_Wolves.jpg", "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')


def layout(id=None):
    # Safe id and data of the observation in global variables
    global observation_id
    global observation_data
    observation_id = id

    if observation_id is not None:
        # Load observation, animal, and location data from database
        observation_data = session.query(Observation).filter_by(id=observation_id).all()[0]
        animal_data = session.query(Animal).filter_by(id=observation_data.animal_id).all()[0]
        location_data = session.query(Location).filter_by(location_number=observation_data.location_id).all()[0]

        return html.Div(
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
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)',
                                'margin': 'auto',
                                'position': 'absolute', 'top': '40%', 'left': '50%',
                                'transform': 'translate(-50%, -50%)'},
                         children=[
                             html.Div(id="alert-output-edit-observation"),
                             html.H1('Edit Observation'),
                             html.Div(
                                 style={'display': 'flex'},
                                 children=[
                                     html.Div(
                                         style={'flex': '50%', 'marginRight': '20px'},
                                         children=[
                                             html.H4('Date'),
                                             html.Div(
                                                 style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'},
                                                 children=[
                                                     html.Div(
                                                         style={'marginBottom': '20px'},
                                                         children=[
                                                             html.Strong('Start Date:', style={'fontWeight': 'bold'}),
                                                             # Input field for start date
                                                             dcc.Input(
                                                                 value=observation_data.start_time.date(),
                                                                 style={'marginLeft': '10px'},
                                                                 disabled=False,
                                                                 id='start-date-input'
                                                             ),
                                                         ]
                                                     ),
                                                     html.Div(
                                                         style={'marginBottom': '20px'},
                                                         children=[
                                                             html.Strong('End Date:', style={'fontWeight': 'bold'}),
                                                             # Input field for end date
                                                             dcc.Input(
                                                                 value=observation_data.end_time.date(),
                                                                 style={'marginLeft': '10px'},
                                                                 disabled=False,
                                                                 id='end-date-input'
                                                             ),
                                                         ]
                                                     ),
                                                     html.H4('Time'),
                                                     html.Div(
                                                         style={'marginBottom': '20px'},
                                                         children=[
                                                             html.Strong('Start Time:', style={'fontWeight': 'bold'}),
                                                             # Input field for start time
                                                             dcc.Input(
                                                                 value=observation_data.start_time.time(),
                                                                 style={'marginLeft': '10px'},
                                                                 disabled=False,
                                                                 id='start-time-input'
                                                             ),
                                                         ]
                                                     ),
                                                     html.Div(
                                                         style={'marginBottom': '20px'},
                                                         children=[
                                                             html.Strong('End Time:', style={'fontWeight': 'bold'}),
                                                             # Input field for end time
                                                             dcc.Input(
                                                                 value=observation_data.end_time.time(),
                                                                 style={'marginLeft': '10px'},
                                                                 disabled=False,
                                                                 id='end-time-input'
                                                             ),
                                                         ]),
                                                 ]),
                                         ]),
                                     html.Div(
                                         style={'flex': '50%'},
                                         children=[
                                             html.H4('Observed Animal'),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Genus:', style={'fontWeight': 'bold'}),
                                                     # Dropdown for animal
                                                     dcc.Dropdown(
                                                         id='edit-genus-dropdown',
                                                         options=[],
                                                         value=animal_data.genus_id,
                                                         placeholder='Select Genus'
                                                     ),
                                                 ]
                                             ),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Animal:', style={'fontWeight': 'bold'}),
                                                     # Dropdown for animal
                                                     dcc.Dropdown(
                                                         id='edit-animal-dropdown',
                                                         options=[],
                                                         value=animal_data.id,
                                                         placeholder='Select Animal'
                                                     ),
                                                 ]
                                             ),
                                             html.H4('Location'),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Location:', style={'fontWeight': 'bold'}),
                                                     # Dropdown for location
                                                     dcc.Dropdown(
                                                         id='edit-location-dropdown',
                                                         options=[],
                                                         value=location_data.location_number,
                                                         placeholder='Select Location'
                                                     ),
                                                 ]),
                                         ]),
                                 ]),
                             html.Div(
                                 style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'},
                                 children=[
                                     html.A(
                                         # Cancel button
                                         html.Button('Cancel', id='cancel-button', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px'}),
                                         href='/view-observation/' + str(observation_id)
                                     ),
                                     html.A(
                                         # Delete button
                                         html.Button('Delete Observation', id='delete-button', n_clicks=0,
                                                     className='btn btn-secondary', style={'padding': '10px 20px'}),
                                         href='/'
                                     ),
                                     html.A(
                                         # Save button
                                         html.Button('Save Changes', id='save-button', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px'}),
                                         href='/view-observation/' + str(observation_id)),
                                 ]
                             ),
                             dcc.Location(id='url-edit-observation'),
                         ]
                         )
            ]
        )
    else:
        return html.Div("No observation ID was provided.")


# Callback executed when page is loaded
@callback(Output('edit-location-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_location_options(pathname):
    if pathname == '/edit-observation/' + str(observation_id):
        # Load latest location options
        return [{'label': l.short_title, 'value': l.location_number} for l in session.query(Location).all()]
    return []


# Callback executed when page is loaded
@callback(Output('edit-genus-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/edit-observation/' + str(observation_id):
        return [{'label': g.species_name, 'value': g.id} for g in session.query(Genus).all()]
    return []


# Callback executed when page is loaded or genus is selected
@callback(Output('edit-animal-dropdown', 'options'),
          [Input('url', 'pathname'),
           Input('edit-genus-dropdown', 'value')])
def update_animal_options(pathname, genus_id):
    if pathname == '/edit-observation/' + str(observation_id):
        return load_animal_options(genus_id)
    return []


# Callback executed when save changes button is clicked
@callback(
    Output('alert-output-edit-observation', 'children'),
    Output('url-edit-observation', 'href'),
    Output('url-edit-observation', 'refresh'),
    [Input('save-button', 'n_clicks')],
    [State('start-date-input', 'value'),
     State('start-time-input', 'value'),
     State('end-date-input', 'value'),
     State('end-time-input', 'value'),
     State('edit-location-dropdown', 'value'),
     State('edit-animal-dropdown', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, spotted_date_start, spotted_time_start, spotted_date_end, spotted_time_end, location,
                 animal):
    if n_clicks is not None:
        # Check if all values are specified
        if spotted_date_start is not None and spotted_date_end is not None and location is not None and animal is not None:

            # Convert date and time to datetime objects
            spotted_date_start = datetime.strptime(f"{spotted_date_start} {spotted_time_start}", '%Y-%m-%d %H:%M:%S')
            spotted_date_end = datetime.strptime(f"{spotted_date_end} {spotted_time_end}", '%Y-%m-%d %H:%M:%S')

            # Show alert if end time is before start time
            if spotted_date_end < spotted_date_start:
                return dbc.Alert(
                    f"End time is before start time!",
                    dismissable=True,
                    color="warning"), '', False

            observation_data.start_time = spotted_date_start
            observation_data.end_time = spotted_date_end
            observation_data.location_id = location
            observation_data.animal_id = animal
            session.commit()
            return '', "'/view-observation/' + str(observation_id)", True
        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False


# Callback executed when delete button is clicked
@callback(
    Output('alert-output-edit-observation', 'children', allow_duplicate=True),
    Output('url-edit-observation', 'href', allow_duplicate=True),
    Output('url-edit-observation', 'refresh', allow_duplicate=True),
    [Input('delete-button', 'n_clicks')],
    prevent_initial_call=True
)
def delete_observation(n_clicks):
    if n_clicks > 0:
        # Delete observation from database
        session.delete(observation_data)
        session.commit()
        return '', '/', True
    else:
        return '', '/edit-observation/' + str(observation_id), False
