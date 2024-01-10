import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output
from models import Animal, Genus
from models import my_session as session
from rpy2.robjects import conversion, default_converter
from rpy2 import robjects as robjects
import plotly.express as px
import pandas as pd

dash.register_page(__name__)


# Function to load analysis data of specific genus from R script
def load_genus_specific_analysis(genus_id):
    with conversion.localconverter(default_converter):
        # Initialize an R session
        r = robjects.r
        # Assign variable to R session
        r.assign('idGenus', genus_id)
        # Run R script
        robjects.r.source('r/genus_specific_analytics.R')
        # Read RDS file containing values from the R script
        r_variables = robjects.r['readRDS']("r/genus_specific.RDS")

        # Safe values of RDS file to variables
        total_animals = r_variables[0]
        specific_animals = r_variables[1]
        max_age_value = r_variables[2]
        percentage_of_animal = str(r_variables[3])

    return total_animals, specific_animals, max_age_value, percentage_of_animal


layout = html.Div([
    html.Div([
        html.H1("Analyze Specific Data", style={'font-weight': 'bold'})
    ], style={'font-family': 'Segoe UI', 'text-align': 'center', 'padding-top': '50px'}),
    # Dropdown with genus
    html.Div([
        dcc.Dropdown(id='genus-dropdown-analysis', options=[], placeholder='Select Animal', value=[], clearable=False),
    ], style={'width': '10%', 'margin': 'auto', 'padding-top': '20px'}),
    # Percentage of animals with selected genus
    html.Plaintext(id='text', style={'text-align': 'center', 'margin-left': '20px'}),
    # Graph with age-groups
    dcc.Graph(id='age_groups', style={'padding-top': '20px'}),
], style={'background-color': 'rgba(224, 238, 224)'})


# Callback executed when page is loaded
@callback(Output('genus-dropdown-analysis', 'options'), Output('genus-dropdown-analysis', 'value'),
          [Input('url', 'pathname')])
def update_animal_options(pathname):
    if pathname == '/analyze-specific-data':
        # Load first genus value in database as default value
        default_genus_value = session.query(Genus).first()
        # Load latest genus options
        return [{'label': g.species_name, 'value': g.id} for g in session.query(Genus).all()], default_genus_value.id
    return [], []


# Callback executed when genus is selected in dropdown
@callback(Output('text', 'children'), Output('age_groups', 'figure'),
          [Input('genus-dropdown-analysis', 'value')])
# Function to generate graph with age-groups
def update_animal_graph_figure(value):
    # Load all analysis values and safe them into variables
    total_animals, specific_animals, max_age_value, percentage_of_animal = load_genus_specific_analysis(value)

    # Load percentage value of selected genus
    split_percentage_result = str(percentage_of_animal).split()[1]
    result_percentage_without_brackets = split_percentage_result.strip('[]')
    specific_genus = session.query(Genus).filter_by(id=value).first()
    text = f'Information: {result_percentage_without_brackets}% of the animals in the database have the genus: {specific_genus.species_name}'

    # Load all ages of animals with selected genus
    all_ages_genus = session.query(Animal.estimated_age).filter_by(genus_id=value).all()

    # Initialize group array
    groups = []
    try:
        # Load groups based on max age value
        groups = build_groups(max_age_value[0])
        # Generate array for counting the number of animals per group
        count_per_group = [0] * len(groups)

        # Loop over every element in groups array
        for group in groups:
            start, end = group

            # Loop over all age values
            for element in all_ages_genus:
                value = element[0]

                # Check if age is part of the group
                if start <= value <= end:
                    count_per_group[groups.index(group)] += 1
    except:
        []

    if len(groups) >= 1:

        string_array = []

        # Format age groups
        for start, end in groups:
            if start == end:
                string_array.append(f"{start} year")
            else:
                string_array.append(f"{start}-{end} years")

        # Create data frame for graph
        data_age_groups = {'Age Group': string_array, 'Number': count_per_group}
        df_age_groups = pd.DataFrame(data_age_groups)

        # Generate graph based on data frame
        fig_age_groups = px.bar(df_age_groups, x='Age Group', y='Number')

        # Update layout of the graph
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
        # Create empty chart if the groups array is empty
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


# Function to generate age groups
def build_groups(zahl):
    # Calculate round number to the nearest multiple of 5
    round_number = ((zahl - 1) // 5 + 1) * 5

    # Calculate edges for grouping
    group_edges = [i for i in range(1, round_number + 1, round_number // 5)]

    # Calculate groups based on edges
    groups = [(group_edges[i], group_edges[i + 1] - 1) for i in range(0, 4)]

    # Calculate the last edge of the group and its corresponding range
    last_edge = int(((round_number / 5) * 4) + 1)

    # Add last edge to groups
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