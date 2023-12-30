import dash
import pandas as pd
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from rpy2 import robjects as robjects

from models import Genus
from models import my_session as session
from rpy2.robjects import conversion, default_converter
import plotly.express as px

dash.register_page(__name__)


# Function to load analysis data from R script
def load_analysis():
    # Load genus data
    genus_data = session.query(Genus).all()

    # Initialize empty arrays
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
            genus_id = genus_value.id
            # Assign variable to R session
            r.assign('idGenus', genus_id)
            # Run R script
            robjects.r.source('genus_analytics.R')
            # Read RDS file containing values from the R script
            r_variables = robjects.r['readRDS']("variables.RDS")

            # Safe values of RDS-file to variables
            # Try except to assign 0 to empty values
            for value in r_variables[0]:
                number_animals_genus.append(int(value))
            genus_names.append(genus_value.species_name)

            for value in r_variables[2]:
                try:
                    genus_average_age.append(int(value))
                except:
                    genus_average_age.append(0)

            for value in r_variables[4]:
                try:
                    genus_average_weight.append(int(value))
                except:
                    genus_average_weight.append(0)

            for value in r_variables[6]:
                try:
                    genus_average_size.append(int(value))
                except:
                    genus_average_size.append(0)

            for value in r_variables[3]:
                try:
                    genus_deviation_age.append(int(value))
                except:
                    genus_deviation_age.append(0)

            for value in r_variables[5]:
                try:
                    genus_deviation_weight.append(int(value))
                except:
                    genus_deviation_weight.append(0)

            for value in r_variables[7]:
                try:
                    genus_deviation_size.append(int(value))
                except:
                    genus_deviation_size.append(0)

            for value in r_variables[8]:
                try:
                    if str(value) != "NA_integer_":
                        genus_median_age.append(int(value))
                    else:
                        genus_median_age.append(0)
                except:
                    genus_median_age.append(0)

            for value in r_variables[1]:
                try:
                    total_animals.append(int(value))
                except:
                    total_animals.append(0)

    return genus_names, number_animals_genus, genus_average_age, genus_average_weight, genus_average_size, genus_deviation_age, genus_deviation_weight, genus_deviation_size, genus_median_age, total_animals


layout = html.Div([
    html.Div([
        html.H1("Analyze Wildlife Data", style={'font-weight': 'bold'})
    ], style={'text-align': 'center', 'padding-top': '50px'}),
    # Div items with two graphs shown in one row
    html.Div([
        html.Div([dcc.Graph(id='number-animal-genus-bar-chart')],
                 style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([dcc.Graph(id='average-age-genus-bar-chart')],
                 style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ]),
    # Div items with two graphs shown in one row
    html.Div([
        html.Div([dcc.Graph(id='average-weight-genus-bar-chart')],
                 style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([dcc.Graph(id='average-size-genus-bar-chart')],
                 style={'width': '50%', 'height': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ]),
], style={'background-color': 'rgba(224, 238, 224)'})


# Callback executed when page is loaded
@callback(Output('number-animal-genus-bar-chart', 'figure'),
          Output('average-age-genus-bar-chart', 'figure'),
          Output('average-weight-genus-bar-chart', 'figure'),
          Output('average-size-genus-bar-chart', 'figure'),
          [Input('url', 'pathname')]
          )
# Function to generate graphs
def update_analysis_all(pathname):
    if pathname == '/analyze-data':
        # Load all analysis values and safe them into variables
        genus_names, genus_numbers, average_age, average_weight, average_size, deviation_age, deviation_weight, deviation_size, median_age, total_numbers = load_analysis()

        # Create data frames for each graph
        data_number = {'Genus': genus_names, 'Number': genus_numbers}
        data_average_median_age = {'Genus': genus_names, 'Average Age': average_age, 'Median Age': median_age}
        data_average_weight = {'Genus': genus_names, 'Average Weight': average_weight}
        data_average_size = {'Genus': genus_names, 'Average Size': average_size}

        df_number = pd.DataFrame(data_number)
        df_average_median_age = pd.DataFrame(data_average_median_age)
        # Melt average and median age in single 'Category' column
        df_average_median_age = pd.melt(df_average_median_age, id_vars='Genus', var_name='Category', value_name='Age')
        df_average_weight = pd.DataFrame(data_average_weight)
        df_average_size = pd.DataFrame(data_average_size)

        # Generate graphs based on data frames
        fig_number = px.bar(df_number, x='Genus', y='Number')
        fig_average_median_age = px.bar(df_average_median_age, x='Genus', y='Age', color='Category', barmode='group',
                                        color_discrete_map={'Average Age': 'rgba(154,205,50,0.8)',
                                                            'Median Age': 'orange'})
        fig_average_weight = px.bar(df_average_weight, x='Genus', y='Average Weight')
        fig_average_size = px.bar(df_average_size, x='Genus', y='Average Size')

        # Update graph layouts
        fig_number.update_layout(
            title=dict(
                text="Number of Animals",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
            ),
            xaxis_title='Genus',
            yaxis_title='Number',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_number.update_traces(
            marker_color='rgba(154,205,50,0.8)'
        )

        fig_average_median_age.update_layout(
            title=dict(
                text="Average and Median Age by Genus",
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font_size=20,
            ),
            legend=dict(
                itemclick=False,
                itemdoubleclick=False,
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
            ),
            legend=dict(
                itemclick=False,
                itemdoubleclick=False,
            ),
            xaxis_title='Genus',
            yaxis_title='Weight in kg',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_weight.update_traces(
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
            ),
            legend=dict(
                itemclick=False,
                itemdoubleclick=False,
            ),
            xaxis_title='Genus',
            yaxis_title='Size in cm',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(224, 238, 224, 1)',
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.5)'),
        )

        fig_average_size.update_traces(
            marker_color='rgba(154,205,50,0.8)'
        )

        # Add lines for standard deviations to graphs
        for fig, lines_data in zip([fig_average_median_age, fig_average_weight, fig_average_size],
                                   [deviation_age, deviation_weight, deviation_size]):
            legend_added = False

            # Add deviation line to every single bar of chart
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
                            showlegend=True,
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
                    # Add legend
                    fig.add_trace(
                        px.scatter(pd.DataFrame({'Genus': [genus_name], 'Standard Deviation': [y_value]}),
                                   x='Genus',
                                   y='Standard Deviation',
                                   opacity=0,
                                   color_discrete_sequence=['red']).data[0]
                    )

        return fig_number, fig_average_median_age, fig_average_weight, fig_average_size
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update