import dash
import pandas as pd
from dash import html, dcc, callback, dash_table, Output, Input
from models import engine

dash.register_page(__name__, path="/")

global observation_id
def load_observations ():
    return pd.read_sql("""SELECT
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
                genus ON animals.genus_id = genus.id
            ORDER BY "End Time" DESC;""", engine)

layout = html.Div(
    style={'backgroundImage': f'url("https://s1.1zoom.me/b6869/14/Forests_Deer_Trees_Fog_557999_1920x1080.jpg")', 'backgroundSize': 'cover','height': '100vh'},
    children=[
        html.H1("Recent Observations",className="display-4 text-center mb-4", style={'font-size': '3em','font-weight': 'bold'}),
    html.Div(id='recent-observations-table')

])

@callback(Output('recent-observations-table', 'children'),
            [Input('url', 'pathname')])
def update_recent_observations(pathname):
    if pathname == '/':
        return html.Table(
            children=[
                # Table Header
                html.Thead(
                    html.Tr([
                        html.Th(col, style={'padding': '12px', 'text-align': 'center', 'font-weight': 'bold', 'background-color': '#343a40', 'color': 'white'}) for col in load_observations().columns
                    ] + [html.Th("Details", style={'padding': '12px', 'margin': '0', 'text-align': 'center', 'font-weight': 'bold', 'background-color': '#343a40', 'color': 'white'})])
                ),
                # Table Body
                html.Tbody([
                    html.Tr([
                        html.Td(str(row[col]), style={'padding': '12px', 'text-align': 'center'}) for col in load_observations().columns
                    ] + [
                        html.Td(html.A("View Details", href=f"/view-observation/{row['ID']}", style={'padding': '12px', 'text-align': 'center'})),
                    ]) for row in load_observations().to_dict('records')
                ])
            ],
            className="table",
            style={'margin': 'auto', 'max-width': '800px', 'overflow': 'hidden'},  # Zentrieren und begrenzte Breite für bessere Lesbarkeit
        )
    return []

