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

# set the layout for edit animal
def layout(id=None):
    global animal_id
    global animal_data
    animal_id = id

    if animal_id is not None:
        animal_data = session.query(Animal).filter_by(id=animal_id).all()[0]
        genus_data = session.query(genus).filter_by(id=animal_data.genus_id).all()[0]

        return html.Div(
            #set a background picture
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover',
                   'backgroundImage': f'url("https://s1.1zoom.me/big0/131/Falcon_Birds_Closeup_falco_tinnunculus_Branches_614759_1280x853.jpg")'
                   },
            # create the table to edit animals
            # create the container
            children=[
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)',
                                'margin': 'auto','position': 'absolute', 'top': '40%', 'left': '50%','transform': 'translate(-50%, -50%)'},
                        children=[
            html.Div(id="alert-output-edit-animal"),
            html.H1('Edit Animal'),

            # create a dropdown to edit gender
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
                                    dcc.Dropdown(
                                        id='gender-edit-dropdown',
                                        options=["Male", "Female", "Diverse"],
                                        value=animal_data.gender,
                                        placeholder='Select Gender'
                                    ),
                                ]),

                            # create a input fiel to edit visual features
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Visual Features:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.visual_features,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='visual-features-edit-input'
                                    ),
                                ]
                            ),
                            # create a input field to edit estimated age
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Age:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_age,
                                        type='number', min=1, step=1,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-age-edit-input'
                                    ),
                                ]
                            ),
                            # create a input field to edit the estimated weight
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Weight:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_weight,
                                        type='number', min=0,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-weight-edit-input'
                                    ),
                                ]
                            ),
                            # create a input field to edit the estimated size
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Estimated Size:', style={'fontWeight': 'bold'}),
                                    dcc.Input(
                                        value=animal_data.estimated_size,
                                        type='number', min=0,
                                        style={'marginLeft': '10px'},
                                        disabled=False,
                                        id='estimated-size-edit-input'
                                    ),
                                ]
                            ),
                            # create a dropdown to edit the genus
                            html.Div(
                                style={'marginBottom': '20px'},
                                children=[
                                    html.Strong('Genus:', style={'fontWeight': 'bold'}),
                                    dcc.Dropdown(
                                        id='genus-edit-dropdown',
                                        options=[],
                                        value=genus_data.id,
                                        placeholder='Select Genus'
                                    ),
                                ]),
                        ]),
                ]),

            # create buttons Cancel Delete and Save
            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between', 'margintop': '20px'},
                children=[
                    html.A(
                        html.Button('Cancel', id='cancel-button', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
                        href='/view-animals'
                    ),
                    html.A(
                        html.Button('Delete Animal', id='delete-button-add-animal', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'})),
                    html.A(
                        html.Button('Save Changes', id='save-button-add-animal', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'})
                    ),
                ]
            ),
            html.Div(id='output-container-animal'),
            dcc.Location(id='url-edit-animal'),
        ]
        )
        ]
        )
    else:
        return html.Div("No animal ID was provided.")


# Callback-Funktion zum Laden der neuesten Location-Optionen
@callback(Output('genus-edit-dropdown', 'options'),
              [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/edit-animal/' + str(animal_id):
        return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]
    return []



# Callback to retrieve values on button click
@callback(
    Output('alert-output-edit-animal', 'children'),
    Output('url-edit-animal', 'href'),
    Output('url-edit-animal', 'refresh'),
    [Input('save-button-add-animal', 'n_clicks')],
    [State('gender-edit-dropdown', 'value'),
     State('visual-features-edit-input', 'value'),
     State('estimated-age-edit-input', 'value'),
     State('estimated-weight-edit-input', 'value'),
     State('estimated-size-edit-input', 'value'),
     State('genus-edit-dropdown', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, gender, visual_features, estimated_age, estimated_weight, estimated_size, genus_id):
    if n_clicks is not None:
        if genus_id is not None and gender is not None and visual_features != '' and estimated_age is not None and estimated_weight is not None and estimated_size is not None and genus_id is not None:
            print("genus_id: " + str(genus_id) + "gender" + str(gender) + "visual_features" + str(visual_features) + "estimated_age" + str(estimated_age) + "estimated_weight" + str(estimated_weight) + "estimated_size" + str(estimated_size))
            animal_data.gender = gender
            animal_data.visual_features = visual_features
            animal_data.estimated_age = estimated_age
            animal_data.estimated_weight = estimated_weight
            animal_data.estimated_size = estimated_size
            animal_data.genus_id = genus_id
            session.commit()
            return '', '/view-animals', True

        else:
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False


# Callback to retrieve values on button click
@callback(
    Output('alert-output-edit-animal', 'children', allow_duplicate=True),
    Output('url-edit-animal', 'href', allow_duplicate=True),
    Output('url-edit-animal', 'refresh', allow_duplicate=True),
    [Input('delete-button-add-animal', 'n_clicks')],
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