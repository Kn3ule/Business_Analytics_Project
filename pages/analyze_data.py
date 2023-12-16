import dash
import pandas as pd
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from rpy2 import robjects as robjects

from models import Animal, Location, genus, base, Observation
from models import my_session as session
from rpy2.robjects import conversion, default_converter
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

def load_analysis(genus_id):

    if genus_id == "all":
        genus_data = session.query(genus).all()

        number_animals_genus = []
        genus_names = []
        genus_average_age = []
        genus_average_weight = []
        genus_average_size = []
        genus_deviation_age = []
        genus_deviation_weight = []
        genus_deviation_size = []
        total_animals = []

        for genus_value in genus_data:
            with conversion.localconverter(default_converter):
                # Initialize an R session
                r = robjects.r
                print("Genus: " + genus_value.species_name)

                genus_id = genus_value.id
                r.assign('idGenus', genus_id)

                robjects.r.source('genus_analytics.R')

                r_variables = robjects.r['readRDS']("variables.RDS")

                for value in r_variables[0]:
                    print("Value: " + str(value))
                    number_animals_genus.append(int(value))
                genus_names.append(genus_value.species_name)

                for value in r_variables[2]:
                    print("AverageAge: " + str(value))
                    try:
                        genus_average_age.append(int(value))
                    except:
                        genus_average_age.append(0)

                for value in r_variables[4]:
                    print("AverageWeight: " + str(value))
                    try:
                        genus_average_weight.append(int(value))
                    except:
                        genus_average_weight.append(0)

                for value in r_variables[6]:
                    print("AverageSize: " + str(value))
                    try:
                        genus_average_size.append(int(value))
                    except:
                        genus_average_size.append(0)

                for value in r_variables[3]:
                    print("DeviationAge: " + str(value))
                    try:
                        genus_deviation_age.append(int(value))
                    except:
                        genus_deviation_age.append(0)

                for value in r_variables[5]:
                    print("DeviationWeight: " + str(value))
                    try:
                        genus_deviation_weight.append(int(value))
                    except:
                        genus_deviation_weight.append(0)

                for value in r_variables[7]:
                    print("DeviationSize: " + str(value))
                    try:
                        genus_deviation_size.append(int(value))
                    except:
                        genus_deviation_size.append(0)

                for value in r_variables[1]:
                    print("TotalNumberAnalyse: " + str(value))
                    try:
                        total_animals.append(int(value))
                    except:
                        total_animals.append(0)

        return genus_names, number_animals_genus, genus_average_age, genus_average_weight, genus_average_size, genus_deviation_age, genus_deviation_weight, genus_deviation_size, total_animals

    return [], [], [], [], [], [], [], [], []

# Layout der Seite zum Hinzufügen von Location
layout = html.Div([
    html.Div([
        html.H1("Analyze Wildlife Data", style={'font-weight': 'bold'})
    ], style={'text-align': 'center', 'padding-top': '50px'}),

    html.Div([
        html.Div([dcc.Graph(id='number-animal-genus-bar-chart')],style={'width': '50%','height': '50%', 'display': 'inline-block','vertical-align': 'top'}),
        html.Div([dcc.Graph(id='average-age-genus-bar-chart')],style={'width': '50%','height': '50%', 'display': 'inline-block','vertical-align': 'top'}),
    ]),
    html.Div([
        html.Div([dcc.Graph(id='average-weight-genus-bar-chart')],style={'width': '50%','height': '50%', 'display': 'inline-block','vertical-align': 'top'}),
        html.Div([dcc.Graph(id='average-size-genus-bar-chart')],style={'width': '50%','height': '50%', 'display': 'inline-block','vertical-align': 'top'}),
    ]),
], style={'background-color': 'rgba(224, 238, 224)'})


@callback(Output('number-animal-genus-bar-chart', 'figure'),
          Output('average-age-genus-bar-chart', 'figure'),
          Output('average-weight-genus-bar-chart', 'figure'),
          Output('average-size-genus-bar-chart', 'figure'),
              [Input('url', 'pathname')]
)


def update_analysis_all(pathname):
    if pathname == '/analyze-data':
        genus_names, genus_numbers, average_age, average_weight, average_size, deviation_age, deviation_weight, deviation_size, total_numbers = load_analysis("all")

        data_number = {'X': genus_names, 'Y': genus_numbers}
        data_average_age = {'X': genus_names, 'Y': average_age}
        data_average_weight = {'X': genus_names, 'Y': average_weight}
        data_average_size = {'X': genus_names, 'Y': average_size}

        df_number = pd.DataFrame(data_number)
        df_average_age = pd.DataFrame(data_average_age)
        df_average_weight = pd.DataFrame(data_average_weight)
        df_average_size = pd.DataFrame(data_average_size)

        fig_number = px.bar(df_number, x='X', y='Y')
        fig_average_age = px.bar(df_average_age, x='X', y='Y')
        fig_average_weight = px.bar(df_average_weight, x='X', y='Y')
        fig_average_size = px.bar(df_average_size, x='X', y='Y')

        fig_number.update_layout(
            title=dict(
                text="Number of Animals",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                #font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Number',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
            #showlegend=True,
        )

        fig_number.update_traces(
            #marker_line=dict(color='white', width=2), #Rand machen
            marker_color = 'rgba(154,205,50,0.8)'
            )

        fig_average_age.update_layout(
            title=dict(
                text="Average Age Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Age',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_age.update_traces(
            # marker_line=dict(color='white', width=2), #Rand machen
            marker_color='rgba(154,205,50,0.8)'
        )

        fig_average_weight.update_layout(
            title=dict(
                text="Average Weight Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Weight',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_weight.update_traces(
            # marker_line=dict(color='white', width=2), #Rand machen
            marker_color='rgba(154,205,50,0.8)'
        )

        fig_average_size.update_layout(
            title=dict(
                text="Average Size Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Size',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_size.update_traces(
            # marker_line=dict(color='white', width=2), #Rand machen
            marker_color='rgba(154,205,50,0.8)'
        )

        for fig, lines_data in zip([fig_average_age, fig_average_weight, fig_average_size],
                                   [deviation_age, deviation_weight, deviation_size]):
            for i, y_value in enumerate(lines_data):
                if y_value != 0:
                    fig.add_shape(
                    type='line',
                    x0=i - 0.4,
                    x1=i + 0.4,
                    y0=y_value,
                    y1=y_value,
                    line=dict(color='red', width=2),
                    )

        return fig_number,fig_average_age,fig_average_weight,fig_average_size
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update