import dash
import pandas as pd
from dash import html, callback, Output, Input
from models import engine

dash.register_page(__name__)

# load animals from database
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
                genus ON animals.genus_id = genus.id
            ORDER BY animals.id;""", engine)


# show animals in a table
layout = html.Div(
    style={'position': 'fixed',
           'top': '10',
           'left': '0',
           'width': '100%',
           'height': '100vh',
           'z-index': '-1',
           'backgroundPosition': 'center',
           'backgroundSize': 'cover',
           'backgroundImage': f'url("https://s1.1zoom.me/big0/479/Rivers_Forests_Mountains_American_bison_Grass_516890_1280x821.jpg")',
           },

    children=[
        html.H1("All Animals", className="display-4 text-center mb-4",
                style={'font-size': '3em', 'font-weight': 'bold', 'padding-top': '40px'}),
        html.Div(id='all-animals-table',
                 style={'overflow-y': 'scroll', 'max-height': '600px', 'margin': 'auto', 'max-width': '800px'})

    ])

# callback executed when page is loaded
@callback(Output('all-animals-table', 'children'),
          [Input('url', 'pathname')])
def update_recent_observations(pathname):
    # if the page is view-animals, the table is loaded
    if pathname == '/view-animals':
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
                                for col in load_animals().columns
                            # add additional column for the details
                            ] + [html.Th("Details", style={'padding': '12px', 'margin': '0', 'text-align': 'center',
                                                           'font-weight': 'bold', 'background-color': '#343a40',
                                                           'color': 'white', 'position': 'sticky', 'top': '0', })])
                ),
                # table body
                html.Tbody([
                    html.Tr([
                                html.Td(str(row[col]), style={'padding': '12px', 'text-align': 'center'}) for col in
                                load_animals().columns
                            ] + [
                                # add link to the edit page of each row
                                html.Td(html.A("Edit animal", href=f"/edit-animal/{row['ID']}",
                                               style={'padding': '12px', 'text-align': 'center'})),
                            ]) for row in load_animals().to_dict('records')
                ])
            ],
        )