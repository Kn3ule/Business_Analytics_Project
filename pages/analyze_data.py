import dash
import pandas as pd
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from pygments.lexers import go
from rpy2 import robjects as robjects
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session
from rpy2.robjects import conversion, default_converter
import plotly.express as px


dash.register_page(__name__)

def load_analysis(genus_id):

    if genus_id == "all":
        genus_data = session.query(genus).all()

        number_animals_genus = []
        genus_names = []


        for genus_value in genus_data:
            with conversion.localconverter(default_converter):
                # Initialize an R session
                r = robjects.r

                genus_id = genus_value.id
                r.assign('idGenus', genus_id)
                r.source("genus_specific_analytics.R")
                r_variables = robjects.r['readRDS']("variables.RDS")
                number_animals_genus.append(int(r_variables[0].replace("[", "").replace("]", "")))
                genus_names.append(genus_value.species_name)

        return number_animals_genus, genus_names


    return [], []


# Layout der Seite zum Hinzufügen von Location
layout = html.Div([
    html.H1("Analyze Wildlife Data"),
    dcc.Graph(id='number-animal-genus-bar-chart')])


@callback(Output('number-animal-genus-bar-chart', 'figure'),
              [Input('url', 'pathname')],
prevent_initial_call = True
)
def update_analysis_all(pathname):
    if pathname == '/analyze-data':
        x_values, y_values = load_analysis("all")
        data = {'X': x_values, 'Y': y_values}
        df = pd.DataFrame(data)
        print(df)
        fig = px.bar(df, x='X', y='Y')
        return fig

    #return px.f