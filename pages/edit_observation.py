import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session

dash.register_page(__name__, path_template='/edit-observation/<id>')

global observation_id
global observation_data

# set the layout for edit genus
def layout(id=None):
    global observation_id
    global observation_data
    observation_id = id

    if observation_id is not None:
        observation_data = session.query(Observation).filter_by(id=observation_id).all()[0]
        animal_data = session.query(Animal).filter_by(id=observation_data.animal_id).all()[0]
        location_data = session.query(Location).filter_by(location_number=observation_data.location_id).all()[0]

        return html.Div(
            # set a background picture
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover','backgroundImage': f'url("https://s1.1zoom.me/big0/945/Forests_Stones_Wolves_498359.jpg")', 'backgroundSize': 'cover',
                   },
            # create the table to edit observation
            # create the container
            children=[
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)','margin': 'auto',
                                'position': 'absolute', 'top': '40%','left': '50%', 'transform': 'translate(-50%, -50%)'},
                         children=[
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

                                            # create input field to edit start date
                                            html.Div(
                                                style={'marginBottom': '20px'},
                                                children=[
                                                    html.Strong('Start Date:', style={'fontWeight': 'bold'}),
                                                    dcc.Input(
                                                        value=observation_data.start_time.date(),
                                                        style={'marginLeft': '10px'},
                                                        disabled=False,  # Enable editing
                                                        id='start-date-input'
                                                        ),
                                                    ]
                                                ),
                                            # create input field to edit end date
                                                html.Div(
                                                    style={'marginBottom': '20px'},
                                                    children=[
                                                        html.Strong('End Date:', style={'fontWeight': 'bold'}),
                                                        dcc.Input(
                                                            value=observation_data.end_time.date(),
                                                            style={'marginLeft': '10px'},
                                                            disabled=False,  # Enable editing
                                                            id='end-date-input'
                                                        ),
                                                    ]
                                                ),
                                                # create input field to edit start time
                                                html.H4('Time'),
                                                html.Div(
                                                    style={'marginBottom': '20px'},
                                                    children=[
                                                        html.Strong('Start Time:', style={'fontWeight': 'bold'}),
                                                        dcc.Input(
                                                            value=observation_data.start_time.time(),
                                                            style={'marginLeft': '10px'},
                                                            disabled=False,  # Enable editing
                                                            id='start-time-input'
                                                        ),
                                                    ]
                                                ),
                                                # create input field to edit end date
                                                html.Div(
                                                    style={'marginBottom': '20px'},
                                                    children=[
                                                        html.Strong('End Time:', style={'fontWeight': 'bold'}),
                                                        dcc.Input(
                                                            value=observation_data.end_time.time(),
                                                            style={'marginLeft': '10px'},
                                                            disabled=False,  # Enable editing
                                                            id='end-time-input'
                                                        ),
                                                    ]),
                                            ]),
                                    ]),
                                     # create dropdown to edit the animal
                                     html.Div(
                                         style={'flex': '50%'},
                                         children=[
                                             html.H4('Observed Animal'),  # Header for Observed Animal Details
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Animal:', style={'fontWeight': 'bold'}),
                                                     dcc.Dropdown(
                                                         id='edit-animal-dropdown',
                                                         options=[],
                                                         value=animal_data.id,
                                                         placeholder='Select Animal'
                                                     ),
                                                 ]
                                             ),

                                             # create a dropdown to edit the location
                                             html.H4('Location'),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Location:', style={'fontWeight': 'bold'}),
                                                     dcc.Dropdown(
                                                         id='edit-location-dropdown',
                                                         options=[],
                                                         value=location_data.location_number,
                                                         placeholder='Select Location'
                                                     ),
                                                 ]),
                                         ]),
                                 ]),

                             # create buttons Cancel Delete and Save
                             html.Div(
                                 style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'},
                                 children=[
                                     html.A(
                                         html.Button('Cancel', id='cancel-button', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px'}),
                                         href='/view-observation/' + str(observation_id)
                                     ),
                                     html.A(
                                         html.Button('Delete Observation', id='delete-button', n_clicks=0,
                                                     className='btn btn-secondary', style={'padding': '10px 20px'}),
                                         href='/'
                                     ),
                                     html.A(
                                         html.Button('Save Changes', id='save-button', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px'}),
                                         href='/view-observation/' + str(observation_id)),
                                 ]
                             ),
                         ]
                         )
            ]
        )
    else:
        return html.Div("No observation ID was provided.")


# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('edit-location-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_location_options(pathname):
    if pathname == '/edit-observation/'+str(observation_id):
        return [{'label': l.short_title, 'value': l.location_number} for l in session.query(Location).all()]
    return []

# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('edit-animal-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_animal_options(pathname):
    if pathname == '/edit-observation/'+str(observation_id):
        return [{'label': a.visual_features, 'value': a.id} for a in session.query(Animal).all()]
    return []


# Callback to retrieve values on button click
@callback(
    Output('output-container', 'children', allow_duplicate=True),
    [Input('save-button', 'n_clicks')],
    [State('start-time-input', 'value'),
     State('end-time-input', 'value'),
     State('edit-location-dropdown', 'value'),
     State('edit-animal-dropdown', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, start_time, end_time, location, animal):
    if n_clicks > 0:
        observation_data.start_time = start_time
        observation_data.end_time = end_time
        observation_data.location_id = location
        observation_data.animal_id = animal
        session.commit()
        print(f'Start Time: {start_time}, End Time: {end_time}, Location: {location}, Animal: {animal}')
    else:
        return ''


# Callback to retrieve values on button click
@callback(
    Output('output-container', 'children', allow_duplicate=True),
    [Input('delete-button', 'n_clicks')],
    prevent_initial_call=True
)
def delete_observation(n_clicks):
    if n_clicks > 0:
        session.delete(observation_data)
        session.commit()
    else:
        return ''