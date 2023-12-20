import dash
import pandas as pd
from dash import html, callback, Output, Input
from models import engine
import base64

dash.register_page(__name__)

# load locations from database
def load_locations():
    return pd.read_sql("""SELECT
            location_number AS "ID",
            short_title AS "Short Title",
            description AS "Description"
            FROM
                locations
            ORDER BY location_number;""", engine)

# Read the local image file and encode it to Base64
with open("./images/island.jpg", "rb") as img_file:
    # richtiges bild: https://s1.1zoom.me/big0/729/USA_Scenery_Autumn_Mountains_Forests_Colorado_617191_1280x640.jpg
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

# show locations in a table
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
        'backgroundImage': f'url("data:image/jpeg;base64,{encoded_image}")',
    },
    children=[
        html.H1("All Locations", className="display-4 text-center mb-4",
                style={'font-size': '3em', 'font-weight': 'bold', 'padding-top': '40px'}),
        html.Div(id='all-locations-table',
                 style={'overflow-y': 'scroll', 'max-height': '600px', 'margin': 'auto', 'max-width': '800px'})
    ])

# callback executed when page is loaded
@callback(Output('all-locations-table', 'children'),
          [Input('url', 'pathname')])
def update_recent_observations(pathname):
    # if the page is view-locations, the table is loaded
    if pathname == '/view-locations':
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
                                for col in load_locations().columns
                            # add additional column for the details
                            ] + [html.Th("Details", style={'padding': '12px', 'margin': '0', 'text-align': 'center',
                                                           'font-weight': 'bold', 'background-color': '#343a40',
                                                           'color': 'white', 'position': 'sticky', 'top': '0', })])
                ),
                # table body
                html.Tbody([
                    html.Tr([
                                html.Td(str(row[col]), style={'padding': '12px', 'text-align': 'center'}) for col in
                                load_locations().columns
                            ] + [
                                # add link to the edit page of each row
                                html.Td(html.A("Edit location", href=f"/edit-location/{row['ID']}",
                                               style={'padding': '12px', 'text-align': 'center'})),
                            ]) for row in load_locations().to_dict('records')
                ])
            ],
        )

