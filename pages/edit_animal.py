import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/edit-animal/<id>')

global animal_id
global animal_data

def layout(id=None):
    global animal_id
    global animal_data
    animal_id = id

    if animal_id is not None:
        animal_data = session.query(Animal).filter_by(id=animal_id).all()[0]
        genus_data = session.query(genus).filter_by(id=animal_data.genus_id).all()[0]


        return html.Div(
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover','backgroundImage': f'url("https://s1.1zoom.me/big0/131/Falcon_Birds_Closeup_falco_tinnunculus_Branches_614759_1280x853.jpg")'
                   },
            children=[
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)',
                                'margin': 'auto','position': 'absolute', 'top': '35%', 'left': '50%','transform': 'translate(-50%, -50%)'},
                        children=[
            html.H1('Edit Animal'),

            html.Div(
                style={'display': 'flex'},
                children=[
                    html.Div(
                        style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'},
                        children=[
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Gender:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.gender,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='gender-input'
                                    ),
                                ]),
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Visual Features:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.visual_features,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='visual-features-input'
                                    ),
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Age:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_age,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-age-input'
                                    ),
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Weight:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_weight,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-weight-input'
                                    ),
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Size:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_size,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-size-input'
                                    ),
                                ]
                            ),
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Genus:', style={'fontWeight': 'bold'}),
                                    dcc.Dropdown(
                                        id='edit-genus-dropdown',
                                        options=[],
                                        value=genus_data.id,
                                        placeholder='Select Genus'
                                    ),
                                ]),
                        ]),
                ]),

            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between', 'margintop': '20px'},
                children=[
                    html.A(
                        html.Button('Cancel', id='cancel-button', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
                        href='/view-animals'
                    ),
                    html.A(
                        html.Button('Delete Animal', id='delete-button', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
                        href='/view-animals'),
                    html.A(
                        html.Button('Save Changes', id='save-button', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
                        href='/view-animals'
                    ),
                ]
            ),

            html.Div(id='output-container-animal', style={'marginTop': '20px'}),
            dcc.Location(id='url-animal'),
        ]
        )
        ]
        )
    else:
        return html.Div("No animal ID was provided.")


# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('edit-genus-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/edit-animal/' + str(animal_id):
        return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]
    return []



# Callback to retrieve values on button click
@callback(
    Output('output-container-animal', 'children', allow_duplicate=True),
    [Input('save-button', 'n_clicks')],
    [State('gender-input', 'value'),
     State('visual-features-input', 'value'),
     State('estimated-age-input', 'value'),
     State('estimated-weight-input', 'value'),
     State('estimated-size-input', 'value'),
     State('edit-genus-dropdown', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, gender, visual_features, estimated_age, estimated_weight, estimated_size, genus):
    if n_clicks > 0:
        animal_data.gender = gender
        animal_data.visual_features = visual_features
        animal_data.estimated_age = estimated_age
        animal_data.estimated_weight = estimated_weight
        animal_data.estimated_size = estimated_size
        animal_data.genus_id = genus
        session.commit()
    else:
        return ''


# Callback to retrieve values on button click
@callback(
    Output('alert-output-animal', 'children', allow_duplicate=True),
    Output('url-animal', 'href'),
    Output('url-animal', 'refresh'),
    [Input('delete-button', 'n_clicks')],
    prevent_initial_call=True
)
def delete_observation(n_clicks):
    if n_clicks > 0:
        # Check if there are no entries with the specified animal id
        observation = session.query(Observation).filter_by(animal_id=animal_id).first()

        if observation is None:
            session.delete(animal_data)
            session.commit()
            return '', '/view-animals', True
        else:
            return dbc.Alert(
                f"Cannot delete animal, because observation with this animal exists.",
                dismissable=True,
                color="warning"), '', False
    else:
        return '', '/edit-animal/' + str(animal_id), False