import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Animal, Location, genus, base, Observation
import os
from datetime import datetime
from models import my_session as session


dash.register_page(__name__, path='/view-observation/')

# Layout der Seite zum Hinzufügen von Location
layout = html.Div([
    html.H1("View Observation Data"),
])