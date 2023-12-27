import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Animal, Genus
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Read the local image file and encode it to Base64
with open("./images/Closeup_Macro_Ladybugs_Insects_Bokeh_Grass.jpg", "rb") as img_file:
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
           'backgroundImage': f'url("data:image/jpeg;base64,{encoded_image}")'
           },
    children=[
        html.Div(
            [
                html.Div(id="alert-output-add-animal"),
                html.H1("Add animal", className="display-4 text-center mb-4",
                        style={'font-size': '3em', 'font-weight': 'bold'}),
                # Dropdowns for genus and gender
                dcc.Dropdown(id='genus-dropdown', options=[], placeholder='Select Genus',
                             className="form-control mb-3"),
                dcc.Dropdown(id='gender-dropdown', options=["Male", "Female", "Diverse"], placeholder='Select Gender',
                             className="form-control mb-3"),
                # Input fields for name, visual features, estimated age, weight and size
                dcc.Input(id='visual-features', type='text', placeholder='Visual Features',
                          className="form-control mb-3"),
                dcc.Input(id='estimated-age', type='number', min=1, step=1, placeholder='Estimated Age (years)',
                          className="form-control mb-3"),
                dcc.Input(id='estimated-weight', type='number', min=0, placeholder='Estimated Weight (kg)',
                          className="form-control mb-3"),
                dcc.Input(id='estimated-size', type='number', min=0, placeholder='Estimated Size (cm)',
                          className="form-control mb-3"),
                # Button to save the animal
                html.Button('Add Animal', id='add-animal-button', className="btn btn-secondary"),
                dcc.Location(id='url-add-animal'),
            ],
            className="container p-5",
            style={'max-width': '600px'}
        )
    ])


# Callback executed when page is loaded
@callback(Output('genus-dropdown', 'options'),
          [Input('url', 'pathname')])
def update_genus_options(pathname):
    if pathname == '/add-animal':
        # Load latest genus options
        return [{'label': g.species_name, 'value': g.id} for g in session.query(Genus).all()]
    return []


# Callback executed when add animal button is clicked
@callback(
    Output('alert-output-add-animal', 'children'),
    Output('url-add-animal', 'href'),
    Output('url-add-animal', 'refresh'),
    [Input('add-animal-button', 'n_clicks')],
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
    if n_clicks is not None:
        # Add animal to database if all values are specified
        if genus_id is not None and gender is not None and visual_features is not None and estimated_age is not None and estimated_weight is not None and estimated_size is not None:
            animal = Animal(
                genus_id=genus_id,
                gender=gender,
                visual_features=visual_features,
                estimated_age=estimated_age,
                estimated_weight=estimated_weight,
                estimated_size=estimated_size
            )
            session.add(animal)
            session.commit()
            return '', '/view-animals', True
        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False
