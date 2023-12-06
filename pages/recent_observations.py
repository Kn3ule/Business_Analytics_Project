import dash
from dash import html, dcc, callback, dash_table
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session
import pandas as pd


#df = pd.DataFrame(session.query(Observation).all(), columns=['id', 'animal_id', 'location_id', 'start_time', 'end_time'])

# Sample data
data = {
    'Animal': ['Hund', 'Reh'],
    'Location': ['New York', 'San Francisco'],
    'Start Time': ['15:30', '10:00'],
    'End Time': ['16:30', '11:00'],
}

# Create a DataFrame from the sample data
df = pd.DataFrame(data)

# Layout der Seite zum Hinzufügen von Location
layout = html.Div([
    html.H1("Recent Observations"),
    dash_table.DataTable(
            id='observations-table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            sort_action='native'
        ),
    html.Div(id='tbl_out'),
    html.Div(id='sort'),
])

@callback(Output('tbl_out', 'children'), Input('observations-table', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"

@callback(
    Output('sort', 'children'),
    Input('observations-table', 'sort_by')
)
def update_sorted_column(sort_by):
    if sort_by:
        sorted_column = sort_by[0]['column_id']
        sort_order = sort_by[0]['direction']
        sort_info = sorted_column + " " + sort_order
        return sort_info
    else:
        return dash.no_update

# For each page, register the layout and callback
dash.register_page(__name__, layout=layout)