import base64

import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Location, Observation
from models import my_session as session
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/edit-location/<id>')

global location_number
global location_data

# Read the local image file and encode it to Base64
with open("./images/Lake_Stones_Forests_Sunrises_and_sunsets_USA.jpg", "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')


def layout(id=None):
    # Safe location_number and data of the location in global variables
    global location_number
    global location_data
    location_number = id

    if location_number is not None:
        # Load location data from database
        location_data = session.query(Location).filter_by(location_number=location_number).all()[0]

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
                                'margin': 'auto', 'position': 'absolute', 'top': '25%', 'left': '50%',
                                'transform': 'translate(-50%, -50%)'},
                         children=[
                             html.Div(id="alert-output-edit-location"),
                             html.H1('Edit Location'),
                             html.Div(
                                 style={'flex': '50%'},
                                 children=[
                                     html.Div(
                                         style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'},
                                         children=[
                                             html.Div(
                                                 style={'marginBottom': '20px'},
                                                 children=[
                                                     html.Strong('Short Title:', style={'fontWeight': 'bold'}),
                                                     # Input field for short title
                                                     dcc.Input(
                                                         value=location_data.short_title,
                                                         style={'marginLeft': '10px'},
                                                         disabled=False,
                                                         id='short-title-input'
                                                     ),
                                                 ]),
                                             html.Div(style={'marginBottom': '20px'},
                                                      children=[
                                                          html.Strong('Description:', style={'fontWeight': 'bold'}),
                                                          # Input field for description
                                                          dcc.Input(
                                                              value=location_data.description,
                                                              style={'marginLeft': '10px'},
                                                              disabled=False,
                                                              id='description-input'
                                                          ),
                                                      ]),
                                         ]),
                                 ]),
                             html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'},
                                      children=[
                                          html.A(
                                              # Cancel button
                                              html.Button('Cancel', id='cancel-button', n_clicks=0,
                                                          className='btn btn-secondary',
                                                          style={'padding': '10px 20px', 'margin': '10px'}),
                                              href='/view-locations'
                                          ),
                                          html.A(
                                              # Delete button
                                              html.Button('Delete Location', id='delete-button-edit-location',
                                                          n_clicks=0, className='btn btn-secondary',
                                                          style={'padding': '10px 20px', 'margin': '10px'})
                                          ),
                                          html.A(
                                              # Save button
                                              html.Button('Save Changes', id='save-button-edit-location', n_clicks=0,
                                                          className='btn btn-secondary',
                                                          style={'padding': '10px 20px', 'margin': '10px'})),
                                      ]),
                             dcc.Location(id='url-edit-location'),
                         ]),
            ])
    else:
        return html.Div("No location number was provided.")


# Callback executed when cancel button is clicked
@callback(
    Output('alert-output-edit-location', 'children'),
    Output('url-edit-location', 'href'),
    Output('url-edit-location', 'refresh'),
    [Input('save-button-edit-location', 'n_clicks')],
    [State('short-title-input', 'value'),
     State('description-input', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, short_title, description):
    if n_clicks is not None:
        # Check if all values are specified
        if short_title != '' and description != '':
            location_data.short_title = short_title
            location_data.description = description
            session.commit()
            return '', '/view-locations', True
        else:
            # Show alert if not all values are specified
            return dbc.Alert(
                f"Please specify all values!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False


# Callback executed when delete button is clicked
@callback(
    Output('alert-output-edit-location', 'children', allow_duplicate=True),
    Output('url-edit-location', 'href', allow_duplicate=True),
    Output('url-edit-location', 'refresh', allow_duplicate=True),
    [Input('delete-button-edit-location', 'n_clicks')],
    prevent_initial_call=True
)
def delete_location(n_clicks):
    if n_clicks is not None:
        # Check if there are no observations with the specified location number
        observation = session.query(Observation).filter_by(location_id=location_number).first()

        if observation is None:
            # Delete location from database
            session.delete(location_data)
            session.commit()
            return '', '/view-locations', True
        else:
            # Show alert if there are observations with the specified location
            return dbc.Alert(
                f"Cannot delete location " + location_data.short_title + ", because observations with this location exists.",
                dismissable=True,
                color="warning"), "", False
    else:
        return '', '/edit-location/' + str(location_number), False
