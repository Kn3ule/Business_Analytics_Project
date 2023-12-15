import dash
from dash import html, dcc
import models
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)


nav2 = dbc.NavbarSimple(
    [
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(page['name'], href=page['path'])
                for page in dash.page_registry.values() if "Add" in page['name'] 
            ],
            nav=True,
            in_navbar=True,
            label="Add Wildlife",
        ),
        dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(page['name'], href=page['path'])
                        for page in dash.page_registry.values() if "View" in page['name'] and "observation" not in page['name']
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Edit Wildlife",
                ),

        dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem(page['name'], href=page['path'])
                        for page in dash.page_registry.values() if "Analyze" in page['name']
                    ],
                    nav=True,
                    in_navbar=True,
                    label="Analyze",
                ),
    ],
    brand="Wildlife Tracker",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        # main app framework
        #html.Div("Wildlife App", style={'fontSize':50, 'textAlign':'center'}),
        nav2,
        #html.Hr(),

        # content of each page
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)