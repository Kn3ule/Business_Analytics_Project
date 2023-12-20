import dash
import pandas as pd
from dash import html, callback, Output, Input
from models import engine

dash.register_page(__name__)

# load genera from database
def load_genera():
    return pd.read_sql("""SELECT
            genus.id AS "ID",
            genus.species_name AS "Species Name"
            FROM
                genus
            ORDER BY genus.id;""", engine)

# show genera in a table
layout = html.Div(
    style={'position': 'fixed',
           'top': '10',
           'left': '0',
           'width': '100%',
           'height': '100vh',
           'z-index': '-1',
           'backgroundPosition': 'center',
           'backgroundSize': 'cover',
           'backgroundImage': f'url("https://windows10spotlight.com/wp-content/uploads/2017/11/6abe548fbb6cbe2449d42b914bd732d9.jpg")',
           },
    children=[
        html.H1("All Genera", className="display-4 text-center mb-4",
                style={'font-size': '3em', 'font-weight': 'bold', 'padding-top': '40px'}),
        html.Div(id='all-genera-table',
                 style={'overflow-y': 'scroll', 'max-height': '600px', 'margin': 'auto', 'max-width': '800px'})
    ])

# callback executed when page is loaded
@callback(Output('all-genera-table', 'children'),
          [Input('url', 'pathname')])
def update_recent_observations(pathname):
    # if the page is view-genera, the table is loaded
    if pathname == '/view-genera':
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
                                for col in load_genera().columns
                            # add additional column for the details
                            ] + [html.Th("Details", style={'padding': '12px', 'margin': '0', 'text-align': 'center',
                                                           'font-weight': 'bold', 'background-color': '#343a40',
                                                           'color': 'white', 'position': 'sticky', 'top': '0', })])
                ),
                # table body
                html.Tbody([
                    html.Tr([
                                html.Td(str(row[col]), style={'padding': '12px', 'text-align': 'center'}) for col in
                                load_genera().columns
                            ] + [
                                # add link to the edit page of each row
                                html.Td(html.A("Edit genus", href=f"/edit-genus/{row['ID']}",
                                               style={'padding': '12px', 'text-align': 'center'})),
                            ]) for row in load_genera().to_dict('records')
                ])
            ],
        )