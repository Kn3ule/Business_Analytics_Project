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

# set the layout for edit genus
def layout(id=None):
    global genus_id
    global genus_data
    genus_id = id

    if genus_id is not None:
        genus_data = session.query(genus).filter_by(id=genus_id).all()[0]
#

        return html.Div(
            # set a background picture
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover',
                   'backgroundImage': f'url("https://s1.1zoom.me/big0/549/Squirrels_Rodents_Bokeh_616888_1280x728.jpg")',
                   },
            # create the table to edit genus
            # create the container
            children=[
            html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)',
                                'margin': 'auto','position': 'absolute', 'top': '20%', 'left': '50%','transform': 'translate(-50%, -50%)'},
                     children=[

    html.H1('Edit Genus'),
    # create input field to edit genus
    html.Div(style={'display': 'flex'},
             children=[
             html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'},
                     children=[
                html.Div(style={'marginBottom': '20px'},
                         children=[
                    html.Div(id="alert-output-edit-genus"),
                    html.Strong('Species Name:', style={'fontWeight': 'bold'}),
                    dcc.Input(
                        value=genus_data.species_name,
                        style={'marginLeft': '10px'},
                        disabled=False,  # Enable editing
                        id = 'species-name-edit-input'
                    ),
                ]),
            ]),
            ]),

    # create buttons Cancel Delete and Save                    # create buttons
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        html.A(
            html.Button('Cancel', id='cancel-button', n_clicks=0, className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'}),
            href='/view-genera'
        ),
        html.A(
            html.Button('Delete Genus', id='delete-button-edit-genus', n_clicks=0,className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'})
        ),
        html.A(
            html.Button('Save Changes', id='save-button-edit-genus', n_clicks=0, className='btn btn-secondary', style={'padding': '10px 20px','margin': '10px'})),
    ]),
    #display putput content
    html.Div(id='output-container-genus'),
    dcc.Location(id='url-edit-genus'),
   ]),
])

    else:
        return html.Div("No genus ID was provided.")



# Callback to retrieve values on button click
@callback(
    Output('alert-output-edit-genus', 'children'),
    Output('url-edit-genus', 'href'),
    Output('url-edit-genus', 'refresh'),
    [Input('save-button-edit-genus', 'n_clicks')],
    [State('species-name-edit-input', 'value')],
    prevent_initial_call=True
)
def save_changes(n_clicks, species_name):
    if n_clicks is not None:
        if species_name is not '':
            genus_data.species_name = species_name
            session.commit()
            return '', '/view-genera', True
        else:
            return dbc.Alert(
                f"Please enter the species name!",
                dismissable=True,
                color="warning"), '', False
    return '', '', False


# Callback to retrieve values on button click
@callback(
    Output('alert-output-edit-genus', 'children', allow_duplicate=True),
    Output('url-edit-genus', 'href', allow_duplicate=True),
    Output('url-edit-genus', 'refresh', allow_duplicate=True),
    [Input('delete-button-edit-genus', 'n_clicks')],
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

