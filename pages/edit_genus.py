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

dash.register_page(__name__, path_template='/edit-genus/<id>')

global genus_id
global genus_data

def layout(id=None):
    global genus_id
    global genus_data
    genus_id = id

    if genus_id is not None:
        genus_data = session.query(genus).filter_by(id=genus_id).all()[0]

        return html.Div(style={'maxWidth': '800px', 'margin': '0 auto', 'padding': '20px'}, children=[
    html.Div(id="alert-output-genus"),
    html.H1('Edit Genus'),  # Header for Observation Details
    html.Div(style={'display': 'flex'}, children=[
        html.Div(style={'flex': '50%', 'marginRight': '20px'}, children=[
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'}, children=[
                html.Div(style={'marginBottom': '20px'}, children=[
                    html.Strong('Species Name:', style={'fontWeight': 'bold'}),
                    dcc.Input(
                        value=genus_data.species_name,
                        style={'marginLeft': '10px'},
                        disabled=False,  # Enable editing
                        id = 'species-input'
                    ),
                ]),
            ]),
        ]),
    ]),
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        html.A(
            html.Button('Cancel', id='cancel-button', n_clicks=0, style={'padding': '10px 20px'}),
            href='/view-genera'
        ),
        html.A(
            html.Button('Delete Genus', id='delete-button', n_clicks=0, style={'padding': '10px 20px'})
        ),
        html.A(
            html.Button('Save Changes', id='save-button', n_clicks=0, style={'padding': '10px 20px'}), href='/view-genera'),
    ]),
    html.Div(id='output-container-genus', style={'marginTop': '20px'}),
    dcc.Location(id='url-genus'),
])
    else:
        return html.Div("No genus ID was provided.")



# Callback to retrieve values on button click
@callback(
    Output('output-container-genus', 'children', allow_duplicate=True),
    [Input('save-button', 'n_clicks')],
    [State('species-name-input', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, species_name):
    if n_clicks > 0:
        genus_data.species_name = species_name
        session.commit()
    else:
        return ''


# Callback to retrieve values on button click
@callback(
    Output('alert-output-genus', 'children', allow_duplicate=True),
    Output('url-genus', 'href'),
    Output('url-genus', 'refresh'),
    [Input('delete-button', 'n_clicks')],
    prevent_initial_call=True
)
def delete_genus(n_clicks):
    if n_clicks > 0:
        # Check if there are no entries with the specified genus id
        animal = session.query(Animal).filter_by(genus_id=genus_id).first()

        if animal is None:
            session.delete(genus_data)
            session.commit()
            return '', '/view-genera', True
        else:
            return dbc.Alert(
                f"Cannot delete genus " + genus_data.species_name + ", because animal with this genus exists.",
                dismissable=True,
                color="warning"), '', False
    else:
        return '', '/edit-genus/' + str(genus_id), False
