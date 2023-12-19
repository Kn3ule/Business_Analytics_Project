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

dash.register_page(__name__, path_template='/edit-location/<id>')

global location_number
global location_data

def layout(id=None):
    global location_number
    global location_data
    location_number = id

    if location_number is not None:
        location_data = session.query(Location).filter_by(location_number=location_number).all()[0]

        return html.Div(
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover','backgroundImage': f'url("https://s1.1zoom.me/big0/849/Lake_Stones_Forests_Sunrises_and_sunsets_USA_600473_1280x853.jpg")'
                   },
            children=[
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)',
                                'margin': 'auto', 'position': 'absolute', 'top': '25%', 'left': '50%',
                                'transform': 'translate(-50%, -50%)'},
                         children=[
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
                        dcc.Input(
                        value=location_data.short_title,
                        style={'marginLeft': '10px'},
                        disabled=False,  # Enable editing
                        id = 'short-title-input'
                    ),
                ]),
                html.Div(style={'marginBottom': '20px'},
                         children=[
                    html.Strong('Description:', style={'fontWeight': 'bold'}),
                    dcc.Input(
                        value=location_data.description,
                        style={'marginLeft': '10px'},
                        disabled=False,  # Enable editing
                        id='description-input'
                    ),
                ]),
            ]),
        ]),

    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        html.A(
            html.Button('Cancel', id='cancel-button', n_clicks=0, className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
            href='/view-locations'
        ),
        html.A(
            html.Button('Delete Location', id='delete-button', n_clicks=0, className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'})
        ),
        html.A(
            html.Button('Save Changes', id='save-button', n_clicks=0, className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}), href='/view-locations'),
    ]),
    html.Div(id='output-container-location', style={'marginTop': '20px'}),
    dcc.Location(id='url-location'),

    ]),
])
    else:
        return html.Div("No location number was provided.")



# Callback to retrieve values on button click
@callback(
    Output('output-container-location', 'children', allow_duplicate=True),
    [Input('save-button', 'n_clicks')],
    [State('short-title-input', 'value'),
     State('description-input', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, short_title, description):
    if n_clicks > 0:
        location_data.short_title = short_title
        location_data.description = description
        session.commit()
    else:
        return ''


# Callback to retrieve values on button click
@callback(
    Output('alert-output-location', 'children', allow_duplicate=True),
    Output('url-location', 'href'),
    Output('url-location', 'refresh'),
    [Input('delete-button', 'n_clicks')],
    prevent_initial_call=True
)
def delete_location(n_clicks):
    if n_clicks > 0:
        # Check if there are no entries with the specified location number
        observation = session.query(Observation).filter_by(location_id=location_number).first()

        if observation is None:
            session.delete(location_data)
            session.commit()
            return '', '/view-locations', True
        else:
            return dbc.Alert(f"Cannot delete location " + location_data.short_title + ", because observations with this location exists.", dismissable=True,
                             color="warning"), "", False
    else:
        return '', '/edit-location/'+str(location_number), False

