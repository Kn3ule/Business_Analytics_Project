import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Animal, Genus, Observation
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/edit-animal/<id>')

global animal_id
global animal_data

# Read the local image file and encode it to Base64
with open("./images/Falcon_Birds_Closeup_falco_tinnunculus_Branches.jpg", "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')


def layout(id=None):
    # Safe id and data of animal in global variables
    global animal_id
    global animal_data
    animal_id = id

    if animal_id is not None:
        # Load animal and genus data from database
        animal_data = session.query(Animal).filter_by(id=animal_id).all()[0]
        genus_data = session.query(Genus).filter_by(id=animal_data.genus_id).all()[0]

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
                                'margin': 'auto', 'position': 'absolute', 'top': '35%', 'left': '50%',
                                'transform': 'translate(-50%, -50%)'},
                         children=[
                             html.Div(id="alert-output-edit-animal"),
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
                                                     # Dropdown for gender
                                                     dcc.Dropdown(
                                                         id='gender-edit-dropdown',
                                                         options=["Male", "Female", "Diverse"],
                                                         value=animal_data.gender,
                                                         placeholder='Select Gender'
                                                     ),
                                                 ]),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Visual Features:', style={'fontWeight': 'bold'}),
                                                     # Input field for visual features
                                                     dcc.Input(
                                                         value=animal_data.visual_features,
                                                         style={'marginLeft': '10px'},
                                                         disabled=False,
                                                         id='visual-features-edit-input'
                                                     ),
                                                 ]
                                             ),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Estimated Age:', style={'fontWeight': 'bold'}),
                                                     # Input field for estimated age
                                                     dcc.Input(
                                                         value=animal_data.estimated_age,
                                                         type='number', min=1, step=1,
                                                         style={'marginLeft': '10px'},
                                                         disabled=False,
                                                         id='estimated-age-edit-input'
                                                     ),
                                                 ]
                                             ),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Estimated Weight:', style={'fontWeight': 'bold'}),
                                                     # Input field for estimated weight
                                                     dcc.Input(
                                                         value=animal_data.estimated_weight,
                                                         type='number', min=0,
                                                         style={'marginLeft': '10px'},
                                                         disabled=False,
                                                         id='estimated-weight-edit-input'
                                                     ),
                                                 ]
                                             ),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Estimated Size:', style={'fontWeight': 'bold'}),
                                                     # Input field for estimated size
                                                     dcc.Input(
                                                         value=animal_data.estimated_size,
                                                         type='number', min=0,
                                                         style={'marginLeft': '10px'},
                                                         disabled=False,
                                                         id='estimated-size-edit-input'
                                                     ),
                                                 ]
                                             ),
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Genus:', style={'fontWeight': 'bold'}),
                                                     # dropdown for genus
                                                     dcc.Dropdown(
                                                         id='genus-edit-dropdown',
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
                                         # Cancel button
                                         html.Button('Cancel', id='cancel-button', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px', 'margin': '10px'}),
                                         href='/view-animals'
                                     ),
                                     html.A(
                                         # Delete button
                                         html.Button('Delete Animal', id='delete-button-add-animal', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px', 'margin': '10px'})),
                                     html.A(
                                         # Save button
                                         html.Button('Save Changes', id='save-button-add-animal', n_clicks=0,
                                                     className='btn btn-secondary',
                                                     style={'padding': '10px 20px', 'margin': '10px'})
                                     ),
                                 ]
                             ),
                             dcc.Location(id='url-edit-animal'),
                         ]
                         )
            ]
        )
    else:
        return html.Div("No animal ID was provided.")


# Callback executed when page is loaded
@callback(Output('genus-edit-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/edit-animal/' + str(animal_id):
        # Load latest genus options
        return [{'label': g.species_name, 'value': g.id} for g in session.query(Genus).all()]
    return []


# Callback executed when save changes button is clicked
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
        # Save changes to database if all values are specified
        if genus_id is not None and gender is not None and visual_features != '' and estimated_age is not None and estimated_weight is not None and estimated_size is not None and genus_id is not None:
            animal_data.gender = gender
            animal_data.visual_features = visual_features
            animal_data.estimated_age = estimated_age
            animal_data.estimated_weight = estimated_weight
            animal_data.estimated_size = estimated_size
            animal_data.genus_id = genus_id
            session.commit()
            return '', '/view-animals', True

        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False


# Callback executed when delete button is clicked
@callback(
    Output('alert-output-edit-animal', 'children', allow_duplicate=True),
    Output('url-edit-animal', 'href', allow_duplicate=True),
    Output('url-edit-animal', 'refresh', allow_duplicate=True),
    [Input('delete-button-add-animal', 'n_clicks')],
    prevent_initial_call=True
)
def delete_animal(n_clicks):
    if n_clicks > 0:
        # Check if there are no observations with the specified animal id
        observation = session.query(Observation).filter_by(animal_id=animal_id).first()

        if observation is None:
            # Delete animal from database
            session.delete(animal_data)
            session.commit()
            return '', '/view-animals', True
        else:
            # Show alert if there are observations with the specified animal
            return dbc.Alert(
                f"Cannot delete animal, because observation with this animal exists.",
                dismissable=True,
                color="warning"), '', False
    else:
        return '', '/edit-animal/' + str(animal_id), False
