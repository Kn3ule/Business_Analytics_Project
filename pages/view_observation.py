import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session


dash.register_page(__name__, path_template='/view-observation/<observation_id>')


def layout(observation_id=None):

    if observation_id is not None:
        observation_data = session.query(Observation).filter_by(id=observation_id).all()[0]
        animal_data = session.query(Animal).filter_by(id=observation_data.animal_id).all()[0]
        location_data = session.query(Location).filter_by(location_number=observation_data.location_id).all()[0]
        genus_data = session.query(genus).filter_by(id=animal_data.genus_id).all()[0]

        return html.Div(
            style={'position': 'fixed',
                   'top': '10',
                   'left': '0',
                   'width': '100%',
                   'height': '100vh',
                   'z-index': '-1',
                   'backgroundPosition': 'center',
                   'backgroundSize': 'cover',
                   'backgroundImage': f'url("https://s1.1zoom.me/big0/962/USA_Rivers_Stones_Forests_Mountains_Crystal_Mill_612749_1280x677.jpg")',
                   },

            children=[
                html.Div(style={'maxWidth': '800px', 'padding': '20px', 'border': '2px solid #ccc',
                                'borderRadius': '10px', 'background-color': 'rgba(255, 255, 255, 0.9)', 'margin': 'auto',
                                'position': 'absolute', 'top': '45%','left': '50%', 'transform': 'translate(-50%, -50%)'
                                },
                         children=[
                             html.H1('Observation Details'),  # Header for Observation Details
                             html.Div(style={'display': 'flex'}, children=[
                                 html.Div(style={'flex': '50%', 'marginRight': '20px'}, children=[
                                              html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'},
                                              children=[
                                                  html.Div(style={'marginBottom': '20px'}, children=[
                                                      html.H4('Date', style={'marginBottom': '10px'}),
                                                      html.Strong('Start Date:', style={'fontWeight': 'bold'}),
                                                      html.Span(observation_data.start_time.date(),
                                                                style={'marginLeft': '10px'})
                                                  ]),
                                                  html.Div(style={'marginBottom': '20px'}, children=[
                                                      html.Strong('End Date:', style={'fontWeight': 'bold'}),
                                                      html.Span(observation_data.end_time.date(),
                                                                style={'marginLeft': '10px'})
                                                  ]),
                                                  html.Div(style={'marginBottom': '20px'}, children=[
                                                      html.H4('Time', style={'marginBottom': '10px'}),
                                                      html.Strong('Start Time:', style={'fontWeight': 'bold'}),
                                                      html.Span(observation_data.start_time.time(),
                                                                style={'marginLeft': '10px'})
                                                  ]),
                                                  html.Div(style={'marginBottom': '20px'}, children=[
                                                      html.Strong('End Time:', style={'fontWeight': 'bold'}),
                                                      html.Span(observation_data.end_time.time(),
                                                                style={'marginLeft': '10px'})
                                                  ]),
                                                  html.Div(style={'marginBottom': '20px'}, children=[
                                                    html.H4(html.Span(location_data.short_title, style={'marginBottom': '10px'})),
                                                    html.Span(location_data.description, style={'marginLeft': '10px'})
                                                  ]),
                                              ]),
                                 ]),
                                 html.Div(style={'flex': '50%'}, children=[
                                     html.H4('Observed Animal'),  # Header for Observed Animal Details
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Gender:', style={'fontWeight': 'bold'}),
                                         html.Span(animal_data.gender, style={'marginLeft': '10px'})
                                     ]),
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Visual Features:', style={'fontWeight': 'bold'}),
                                         html.Span(animal_data.visual_features, style={'marginLeft': '10px'})
                                     ]),
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Estimated Age:', style={'fontWeight': 'bold'}),
                                         html.Span(animal_data.estimated_age, style={'marginLeft': '10px'})
                                     ]),
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Estimated Weight:', style={'fontWeight': 'bold'}),
                                         html.Span(animal_data.estimated_weight, style={'marginLeft': '10px'})
                                     ]),
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Estimated Size:', style={'fontWeight': 'bold'}),
                                         html.Span(animal_data.estimated_size, style={'marginLeft': '10px'})
                                     ]),
                                     html.Div(style={'marginBottom': '20px'}, children=[
                                         html.Strong('Genus:', style={'fontWeight': 'bold'}),
                                         html.Span(genus_data.species_name, style={'marginLeft': '10px'})
                                     ]),
                                 ]),
                             ]),
                             html.Div(style={'textAlign': 'left', 'marginTop': '20px'}, children=[
                                 html.A(
                                     html.Button('Edit Observation', id='edit-button', n_clicks=0,
                                                 className='btn btn-secondary',
                                                 style={'padding': '10px 20px'}),
                                     href='/edit-observation/' + str(observation_id)),
                             ]),
                         ])
            ])


    else:
        return html.Div("No observation ID was provided.")