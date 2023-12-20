import dash
import pandas as pd
from dash import html, callback, Output, Input
from models import engine

dash.register_page(__name__, path="/")

# load observations from database
def load_observations():
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

# show observations in a table
layout = html.Div(
    style={
        'position': 'fixed',
        'top': '10',
        'left': '0',
        'width': '100%',
        'height': '100vh',
        'z-index': '-1',
        'backgroundPosition': 'center',
        'backgroundSize': 'cover',
        'backgroundImage': f'url("https://s1.1zoom.me/big0/391/Woodpecker_Birds_Bokeh_612016_1280x853.jpg")'
    },
    children=[
        html.H1("Recent Observations", className="display-4 text-center mb-4",
                style={'font-size': '3em', 'font-weight': 'bold', 'padding-top': '30px'}),
        html.Div(id='recent-observations-table',
                 style={'overflow-y': 'scroll', 'max-height': '600px', 'margin': 'auto', 'max-width': '800px'})

    ])

# callback executed when page is loaded
@callback(Output('recent-observations-table', 'children'),
          [Input('url', 'pathname')])
def update_recent_observations(pathname):
    # if the page is the start page, the table is loaded
    if pathname == '/':
        return html.Table(
            className="table",
            style={'opacity': '0.9'},
            children=[
                # table header
                html.Thead(
                    html.Tr([
                                html.Th(col, style={'padding': '12px', 'text-align': 'center', 'font-weight': 'bold',
                                                    'background-color': '#343a40', 'color': 'white',
                                                    'position': 'sticky', 'top': '0'})
                                for col in load_observations().columns
                            # add additional column for details
                            ] + [html.Th("Details", style={'padding': '12px', 'margin': '0', 'text-align': 'center',
                                                           'font-weight': 'bold',
                                                           'background-color': '#343a40', 'color': 'white',
                                                           'position': 'sticky', 'top': '0'})])
                ),
                # table body
                html.Tbody([
                    html.Tr([
                                html.Td(str(row[col]), style={'padding': '12px', 'text-align': 'center'}) for col in
                                load_observations().columns
                            ] + [
                                # add link to the edit page of each row
                                html.Td(html.A("View Details", href=f"/view-observation/{row['ID']}",
                                               style={'padding': '12px', 'text-align': 'center'})),
                            ]) for row in load_observations().to_dict('records')
                ])
            ],
        )