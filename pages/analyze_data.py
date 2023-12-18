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
        genus_median_age = []
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

                for value in r_variables[8]:
                    print("MedianAge: " + str(value))
                    try:
                        genus_median_age.append(int(value))
                    except:
                        genus_median_age.append(0)

                for value in r_variables[1]:
                    print("TotalNumberAnalyse: " + str(value))
                    try:
                        total_animals.append(int(value))
                    except:
                        total_animals.append(0)

        return genus_names, number_animals_genus, genus_average_age, genus_average_weight, genus_average_size, genus_deviation_age, genus_deviation_weight, genus_deviation_size, genus_median_age, total_animals

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
        genus_names, genus_numbers, average_age, average_weight, average_size, deviation_age, deviation_weight, deviation_size, median_age, total_numbers = load_analysis("all")

        data_number = {'Genus': genus_names, 'Number': genus_numbers}
        data_average_median_age = {'Genus': genus_names, 'Average Age': average_age, 'Median Age': median_age}
        data_average_weight = {'Genus': genus_names, 'Average Weight': average_weight}
        data_average_size = {'Genus': genus_names, 'Average Size': average_size}

        df_number = pd.DataFrame(data_number)
        df_average_median_age = pd.DataFrame(data_average_median_age)
        # Melt the DataFrame to have a single 'Age Type' column (Average Age, Median Age)
        df_average_median_age = pd.melt(df_average_median_age, id_vars='Genus', var_name='Age Type', value_name='Age')
        df_average_weight = pd.DataFrame(data_average_weight)
        df_average_size = pd.DataFrame(data_average_size)

        fig_number = px.bar(df_number, x='Genus', y='Number')
        fig_average_median_age = px.bar(df_average_median_age, x='Genus', y='Age', color='Age Type', barmode='group', color_discrete_map={'Average Age': 'rgba(154,205,50,0.8)', 'Median Age': 'orange'})

        fig_average_weight = px.bar(df_average_weight, x='Genus', y='Average Weight')
        fig_average_size = px.bar(df_average_size, x='Genus', y='Average Size')

        fig_number.update_layout(
            title=dict(
                text="Number of Animals",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
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

        fig_average_median_age.update_layout(
            title=dict(
                text="Average and Median Age by Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Average Age',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_weight.update_layout(
            title=dict(
                text="Average Weight Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Weight in kg',
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
                font_size=20,
                # font=dict(size=18, color='black', weight='bold')
            ),
            xaxis_title='Genus',
            yaxis_title='Size in cm',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_size.update_traces(
            # marker_line=dict(color='white', width=2), #Rand machen
            marker_color='rgba(154,205,50,0.8)'
        )

        for fig, lines_data in zip([fig_average_median_age, fig_average_weight, fig_average_size],
                                   [deviation_age, deviation_weight, deviation_size]):
            legend_added = False

            for i, (y_value, genus_name) in enumerate(zip(lines_data, genus_names)):
                if y_value != 0:
                    if not legend_added:
                        fig.add_shape(
                        type='line',
                        x0=i - 0.4,
                        x1=i + 0.4,
                        y0=y_value,
                        y1=y_value,
                        line=dict(color='red', width=2),
                        name='Standard Deviation',
                        showlegend=True
                        )
                        legend_added = True
                    else:
                        fig.add_shape(
                            type='line',
                            x0=i - 0.4,
                            x1=i + 0.4,
                            y0=y_value,
                            y1=y_value,
                            line=dict(color='red', width=2)
                        )
                    fig.add_trace(
                        px.scatter(pd.DataFrame({'Genus': genus_names, 'Standard Deviation': y_value}),
                                   x='Genus',
                                   y='Standard Deviation',
                                   opacity=0,
                                   color_discrete_sequence=['red']).data[0]
                    )


        return fig_number,fig_average_median_age,fig_average_weight,fig_average_size
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update