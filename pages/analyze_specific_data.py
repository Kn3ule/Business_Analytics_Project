import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session
import dash_bootstrap_components as dbc
from rpy2.robjects import conversion, default_converter
from rpy2 import robjects as robjects
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

def load_genus_specific_analysis(start, genus_id):

    if start == "specific":
        with conversion.localconverter(default_converter):
            # Initialize an R session
            r = robjects.r
            r.assign('idGenus', genus_id)
            robjects.r.source('genus_specific_analytics.R')
            r_variables = robjects.r['readRDS']("genus_specific.RDS")

            total_animals = r_variables[0]
            specific_animals = r_variables[1]
            max_age_value = r_variables[2]
            percentage_of_animal=str(r_variables[3])

    return total_animals, specific_animals, max_age_value, percentage_of_animal


layout = html.Div([
    html.Div([
        html.H1("Analyze Specific Data", style={'font-weight': 'bold'})
    ], style={'font-family':'Segoe UI', 'text-align': 'center', 'padding-top': '50px'}),
    html.Div([
        dcc.Dropdown(id='genus-dropdown-analysis', options=[], placeholder='Select Animal', value=[], clearable=False),
    ],style={'width': '10%','margin': 'auto','padding-top': '20px'}),
    html.Plaintext(id='test', style={'text-align': 'center', 'margin-left':'20px'}),
    dcc.Graph(id='age_groups', style={'padding-top': '20px'}),
],style={'background-color': 'rgba(224, 238, 224)'})

def load_genus_options():
    return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]

@callback(Output('genus-dropdown-analysis', 'options'),Output('genus-dropdown-analysis', 'value'),
              [Input('url', 'pathname')])

def update_animal_options(pathname):
    if pathname == '/analyze-specific-data':
        default_genus_value = session.query(genus).first()
        return load_genus_options(), default_genus_value.id
    return [], []

@callback(Output('test', 'children'),Output('age_groups', 'figure'),
              [Input('genus-dropdown-analysis', 'value')])

def update_animal_graph_figure(value):

    total_animals, specific_animals, max_age_value, percentage_of_animal = load_genus_specific_analysis("specific",value)

    specific_genus = session.query(genus).filter_by(id=value).first()
    percentage = round((specific_animals[0]/total_animals[0])*100,2) #R-Skript-Funktion bereits vorhanden
    text=f'Information: {percentage}% of the animals in the database have the genus: {specific_genus.species_name}'

    all_ages_genus = session.query(Animal.estimated_age).filter_by(genus_id=value).all()
    gruppen = []
    try:
        gruppen = gruppiere_zahlen(max_age_value[0])

        count_per_group = [0] * len(gruppen)

        # Iteriere über jedes Element im zweiten Array
        for group in gruppen:
            start, end = group

            # Iteriere über jedes Element im Ursprungsarray
            for element in all_ages_genus:
                value = element[0]  # Nehme die Zahl aus dem Ursprungsarray

                # Überprüfe, ob die Zahl innerhalb der Range liegt
                if start <= value < end:
                    count_per_group[gruppen.index(group)] += 1
    except:
        []

    print(gruppen)

    if len(gruppen) >= 1:
        string_array = []
        for start, end in gruppen:
            if start == end:
                string_array.append(f"{start} year")
            else:
                string_array.append(f"{start}-{end} years")

        data_age_groups = {'Age Group': string_array, 'Number': count_per_group}
        df_age_groups = pd.DataFrame(data_age_groups)
        fig_age_groups = px.bar(df_age_groups, x='Age Group', y='Number')

        fig_age_groups.update_layout(
            title=dict(
                text="Age-Groups of a specific animal",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
            ),
            xaxis_title='Age Groups',
            yaxis_title='Number',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)', dtick=1),
        )

        fig_age_groups.update_traces(
            marker_color='rgba(154,205,50,0.8)'
        )
    else:
        data_age_groups = {'Age Group': [0], 'Number': [0]}
        df_age_groups = pd.DataFrame(data_age_groups)
        fig_age_groups = px.bar(df_age_groups, x='Age Group', y='Number')

        fig_age_groups.update_layout(
            title=dict(
                text="No data available",
                x=0.5,
                y=0.55,
                xanchor='center',
                yanchor='top',
                font_size=20,
            ),
            xaxis_title='Age-Groups',
            yaxis_title='Number',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=False)
        )
    return text, fig_age_groups

def gruppiere_zahlen(zahl):
    if zahl == 0:
        zahl = 1
    gerundete_zahl = ((zahl - 1) // 5 + 1) * 5
    # Berechne die Gruppengrenzen
    gruppen_grenzen = [i for i in range(1, gerundete_zahl + 1, gerundete_zahl // 5)]
    # Erstelle die Gruppen
    gruppen = [(gruppen_grenzen[i]-1,gruppen_grenzen[i + 1] - 1) for i in range(0, 4)]

    # letzte Grenze manuell setzen
    letzteGrenze = int(((gerundete_zahl/5)*4)+1)
    gruppen.append((letzteGrenze,int((letzteGrenze+(gerundete_zahl/5))-1)))

    return gruppen

