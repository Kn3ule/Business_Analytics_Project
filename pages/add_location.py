import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from models import Location
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Read the local image file and encode it to Base64
with open("./images/Finland_Parks_Forests_Rivers_Oulanka_National_Park.jpg", "rb") as img_file:
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
                html.Div(id="alert-output-add-location"),
                html.H1("Add Location", className="display-4 text-center mb-4",
                        style={'font-size': '3em', 'font-weight': 'bold'}),
                # Input fields for short title and description of location
                dcc.Input(id='short-title', type='text', placeholder='Short Title', className="form-control mb-3"),
                dcc.Input(id='description', type='text', placeholder='Description', className="form-control mb-3"),
                # Button to save the location
                html.Button('Add Location', id='add-location-button', className="btn btn-secondary"),
                dcc.Location(id='url-add-location')
            ],
            className="container p-5",
            style={'max-width': '600px'}
        )
    ])


# Callback executed when add location button is clicked
@callback(
    Output('alert-output-add-location', 'children'),
    Output('url-add-location', 'href'),
    Output('url-add-location', 'refresh'),
    [Input('add-location-button', 'n_clicks')],
    [dash.dependencies.State('short-title', 'value'),
     dash.dependencies.State('description', 'value')]
)
def add_location(n_clicks, short_title, description):
    if n_clicks is not None:
        # Add location to database if short title and description are specified
        if short_title is not None and description is not None:
            new_location = Location(short_title=short_title, description=description)
            session.add(new_location)
            session.commit()
            return '', '/view-locations', True
        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False
