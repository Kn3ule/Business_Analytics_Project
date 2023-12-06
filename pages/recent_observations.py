import dash
import pandas as pd
from dash import html, dcc, callback, dash_table, Output, Input
from models import engine

dash.register_page(__name__, path="/")


df_observations = pd.read_sql("""SELECT
    observations.id AS "ID",
    TO_CHAR(observations.start_time, 'YYYY-MM-DD HH24:MI:SS') AS "Start Time",
    TO_CHAR(observations.end_time, 'YYYY-MM-DD HH24:MI:SS') AS "End Time",
    animals.visual_features AS "Visual Features",
    genus.species_name AS "Species",
    locations.short_title AS "Location"
    FROM
        observations
    JOIN
        animals ON observations.animal_id = animals.id
    JOIN
        locations ON observations.location_id = locations.location_number
    JOIN
        genus ON animals.genus_id = genus.id;""", engine)

layout = html.Div([
    html.H1("Recent Observations"),
    html.Table(children=[
        html.Tr([html.Th(col, style={'padding': '8px'}) for col in df_observations.columns] + [html.Th("Details", style={'padding': '8px', 'margin': '0'})]),
        *[
            html.Tr([
                html.Td(str(row[col]), style={'padding': '8px'}) for col in df_observations.columns
            ] + [
                html.Td(html.A("View Details", href=f"/view-observation/{row['ID']}", style={'padding': '8px'}))  # Replace 'id' with your unique identifier
            ]) for row in df_observations.to_dict('records')
        ]
    ], style={'border-spacing': '10px'})
])