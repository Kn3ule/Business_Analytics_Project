import dash
import pandas as pd
from dash import html, dcc, callback, dash_table, Output, Input
from models import engine

dash.register_page(__name__)

global observation_id
def load_locations():
    return pd.read_sql("""SELECT
            location_number AS "ID",
            short_title AS "Short Title",
            description AS "Description"
            FROM
                locations;""", engine)

layout = html.Div([
    html.H1("All Locations"),
    html.Div(id='all-locations-table'),
    html.Div(id='locations-output'),
])

@callback(Output('all-locations-table', 'children'),
            [Input('url', 'pathname')])
def update_recent_observations(pathname):
    if pathname == '/view-locations':
        return html.Table(children=[
        html.Tr([html.Th(col, style={'padding': '8px'}) for col in load_locations().columns] + [html.Th("Edit", style={'padding': '8px', 'margin': '0'})]),
        *[
            html.Tr([
                html.Td(str(row[col]), style={'padding': '8px'}) for col in load_locations().columns
            ] + [
                html.Td(html.A("Edit Location", href=f"/edit-location/{row['ID']}", style={'padding': '8px'})),  # Replace 'id' with your unique identifier
            ]) for row in load_locations().to_dict('records')
        ]
        ], style={'border-spacing': '10px'})
    return []

