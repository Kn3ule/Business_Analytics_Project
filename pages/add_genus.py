import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from models import Genus
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Read the local image file and encode it to Base64
with open("./images/Blackangel.jpg", "rb") as img_file:
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
           'backgroundImage': f'url("data:image/jpeg;base64,{encoded_image}")'},
    children=[
        html.Div(
            [
                html.Div(id="alert-output-add-genus"),
                html.H1("Add Genus", className="display-4 text-center mb-4",
                        style={'font-size': '3em', 'font-weight': 'bold'}),
                # Input field for species name
                dcc.Input(id='species-name', type='text', placeholder='Species Name', className="form-control mb-3"),
                # Button to save the genus
                html.Button('Add Genus', id='add-genus-button', className="btn btn-secondary"),
                dcc.Location(id='url-add-genus')
            ],
            className="container p-5",
            style={'max-width': '600px'}
        )
    ])


# Callback executed when add genus button is clicked
@callback(
    Output('alert-output-add-genus', 'children'),
    Output('url-add-genus', 'href'),
    Output('url-add-genus', 'refresh'),
    [Input('add-genus-button', 'n_clicks')],
    [dash.dependencies.State('species-name', 'value')]
)
def safe_genus(n_clicks, species_name):
    if n_clicks is not None:
        # Add genus to database if species name is specified
        if species_name is not None:
            new_genus = Genus(species_name=species_name)
            session.add(new_genus)
            session.commit()
            return '', '/view-genera', True
        else:
            # Show alert if species name is not specified
            return dbc.Alert(
                f"Please enter the species name!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False
