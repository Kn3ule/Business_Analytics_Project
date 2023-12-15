import dash
import pandas as pd
from dash import html, dcc, callback, dash_table, Output, Input
from models import engine

dash.register_page(__name__)

global observation_id
def load_animals():
    return pd.read_sql("""SELECT
            animals.id AS "ID",
            genus.species_name AS "Species Name",
            animals.gender AS "Gender",
            animals.visual_features AS "Visual Features",
            animals.estimated_age AS "Estimated Age",
            animals.estimated_weight AS "Estimated Weight",
            animals.estimated_size AS "Estimated Size"
            FROM
                animals
            JOIN
                genus ON animals.genus_id = genus.id;""", engine)

layout = html.Div([
    html.H1("All Animals"),
    html.Div(id='all-animals-table')
])

@callback(Output('all-animals-table', 'children'),
            [Input('url', 'pathname')])
def update_recent_observations(pathname):
    if pathname == '/view-animals':
        return html.Table(children=[
        html.Tr([html.Th(col, style={'padding': '8px'}) for col in load_animals().columns] + [html.Th("Edit", style={'padding': '8px', 'margin': '0'})]),
        *[
            html.Tr([
                html.Td(str(row[col]), style={'padding': '8px'}) for col in load_animals().columns
            ] + [
                html.Td(html.A("Edit Animal", href=f"/edit-animal/{row['ID']}", style={'padding': '8px'})),  # Replace 'id' with your unique identifier
            ]) for row in load_animals().to_dict('records')
        ]
        ], style={'border-spacing': '10px'})
    return []

