import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from models import Animal, Location, genus, base, Observation
from models import my_session as session
from rpy2.robjects import conversion, default_converter
from rpy2 import robjects as robjects
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

# Function to analyse specific genus data
def load_genus_specific_analysis(start, genus_id):
    if start == "specific":
        with conversion.localconverter(default_converter):
            # Initialize an R session
            r = robjects.r
            # Assign variable to R session
            r.assign('idGenus', genus_id)
            # Run R-Skript
            robjects.r.source('genus_specific_analytics.R')
            # Read RDS-File - outcome of Run R-Skript
            r_variables = robjects.r['readRDS']("genus_specific.RDS")

            # Safe RDS-File values to variables
            total_animals = r_variables[0]
            specific_animals = r_variables[1]
            max_age_value = r_variables[2]
            percentage_of_animal = str(r_variables[3])

    return total_animals, specific_animals, max_age_value, percentage_of_animal


# Page Layout
layout = html.Div([
    # Header
    html.Div([
        html.H1("Analyze Specific Data", style={'font-weight': 'bold'})
    ], style={'font-family': 'Segoe UI', 'text-align': 'center', 'padding-top': '50px'}),
    # Dropdown with dynamic options and default value
    html.Div([
        dcc.Dropdown(id='genus-dropdown-analysis', options=[], placeholder='Select Animal', value=[], clearable=False),
    ], style={'width': '10%', 'margin': 'auto', 'padding-top': '20px'}),
    # Information about percentage of specific animals
    html.Plaintext(id='text', style={'text-align': 'center', 'margin-left': '20px'}),
    # Age-Groups Graph
    dcc.Graph(id='age_groups', style={'padding-top': '20px'}),
], style={'background-color': 'rgba(224, 238, 224)'})


# Function to load the dropdown data
def load_genus_options():
    return [{'label': g.species_name, 'value': g.id} for g in session.query(genus).all()]


# Callback on path with output options for dropdown and default value dropdown
@callback(Output('genus-dropdown-analysis', 'options'), Output('genus-dropdown-analysis', 'value'),
          [Input('url', 'pathname')])
# Call function to get dropdown genus options and dropdown default value
def update_animal_options(pathname):
    if pathname == '/analyze-specific-data':
        default_genus_value = session.query(genus).first()
        return load_genus_options(), default_genus_value.id
    return [], []


# Callback on selected dropdown value with figure and text as an output
@callback(Output('text', 'children'), Output('age_groups', 'figure'),
          [Input('genus-dropdown-analysis', 'value')])

# Function to generate graph
def update_animal_graph_figure(value):
    # Trigger function to load all values and safe it into variables
    total_animals, specific_animals, max_age_value, percentage_of_animal = load_genus_specific_analysis("specific",
                                                                                                        value)
    # Preperation of percentage value
    split_percentage_result = str(percentage_of_animal).split()[1]
    result_percentage_without_brackets = split_percentage_result.strip('[]')

    specific_genus = session.query(genus).filter_by(id=value).first()
    text = f'Information: {result_percentage_without_brackets}% of the animals in the database have the genus: {specific_genus.species_name}'

    # Get all ages of specific animals
    all_ages_genus = session.query(Animal.estimated_age).filter_by(genus_id=value).all()

    # Initialize group array
    groups = []
    try:
        # Call function
        groups = build_groups(max_age_value[0])
        # Generate Array with specific number of elements
        count_per_group = [0] * len(groups)

        # Loop for every element in groups array
        for group in groups:
            start, end = group

            # Loop for every value inside our elements of the all_ages_genus array
            for element in all_ages_genus:
                value = element[0]

                # Check if the all_ages_genus element is part of the element in groups array
                if start <= value <= end:
                    count_per_group[groups.index(group)] += 1
    except:
        []

    # Condition to generate x-axis text
    if len(groups) >= 1:
        # Initialize string_array
        string_array = []
        # Check difference of elements in groups array to generate x-axis text
        for start, end in groups:
            if start == end:
                string_array.append(f"{start} year")
            else:
                string_array.append(f"{start}-{end} years")

        data_age_groups = {'Age Group': string_array, 'Number': count_per_group}
        df_age_groups = pd.DataFrame(data_age_groups)

        fig_age_groups = px.bar(df_age_groups, x='Age Group', y='Number')

        # Modify the layout of the figure
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
        # If the groups array is empty
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


# Function to generate all the groups
def build_groups(zahl):
    round_number = ((zahl - 1) // 5 + 1) * 5
    # Calculate edges
    group_edges = [i for i in range(1, round_number + 1, round_number // 5)]
    # Generate groups
    groups = [(group_edges[i], group_edges[i + 1] - 1) for i in range(0, 4)]
    last_edge = int(((round_number / 5) * 4) + 1)
    groups.append((last_edge, int((last_edge + (round_number / 5)) - 1)))

    return groups

'''
def gruppiere_zahlen(max_age):
    #if zahl == 0:
        #zahl = 1
    
    span = math.ceil(max_age / 5)
    # Erstellen der Altersgruppen mit exklusiver Obergrenze
    age_groups = [(i, min(i + span, max_age)) for i in range(0, max_age, span)]
    print(age_groups)

    # Anpassen der Gruppen, um Überschneidungen zu vermeiden
    # Die untere Grenze jeder Gruppe (außer der ersten) wird um 1 erhöht
    adjusted_age_groups = [age_groups[0]] + [(age_groups[i][0] + 1, age_groups[i][1]) for i in range(1, 5)]
    

    return adjusted_age_groups
'''
