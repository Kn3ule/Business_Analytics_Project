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

dash.register_page(__name__)

layout = html.Div([
    html.H1("All Animals"),
    dcc.Dropdown(id='genus-dropdown-analysis', options=[], placeholder='Select Animal', className="form-control mb-3"),
    dcc.Graph(id='genus-graph'),
])

def load_genus_options():

    return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]


@callback(Output('genus-dropdown-analysis', 'options'),
              [Input('url', 'pathname')])
def update_animal_options(pathname):
    if pathname == '/analyze-specific-data':
        return load_genus_options()
    return []

@callback(Output('genus-graph', 'children'),
                [Input('genus-dropdown', 'options')])
def update_animal_graph(genus_options):
    return dcc.Graph(id='genus-graph', figure={
        'data': [{
            'x': [1, 2, 3],
            'y': [4, 1, 2],
            'type': 'bar'
        }],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    })
