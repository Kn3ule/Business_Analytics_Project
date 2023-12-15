import dash
import pandas as pd
from dash import html, dcc, callback, dash_table, Output, Input
from models import engine

dash.register_page(__name__)

global observation_id
def load_genera():
    return pd.read_sql("""SELECT
            genus.id AS "ID",
            genus.species_name AS "Species Name"
            FROM
                genus;""", engine)

layout = html.Div([
    html.H1("All Genera"),
    html.Div(id='all-genera-table')
])

@callback(Output('all-genera-table', 'children'),
            [Input('url', 'pathname')])
def update_recent_observations(pathname):
    if pathname == '/view-genera':
        return html.Table(children=[
        html.Tr([html.Th(col, style={'padding': '8px'}) for col in load_genera().columns] + [html.Th("Edit", style={'padding': '8px', 'margin': '0'})]),
        *[
            html.Tr([
                html.Td(str(row[col]), style={'padding': '8px'}) for col in load_genera().columns
            ] + [
                html.Td(html.A("Edit Genus", href=f"/edit-genus/{row['ID']}", style={'padding': '8px'})),  # Replace 'id' with your unique identifier
            ]) for row in load_genera().to_dict('records')
        ]
        ], style={'border-spacing': '10px'})
    return []

