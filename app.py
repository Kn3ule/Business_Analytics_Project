import dash
from dash import html, dcc, Output, Input
import models
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        # main app framework
        html.Div("Wildlife Management", style={'fontSize': 50, 'textAlign': 'center'}),

        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label=page['name'], value=page['path'])
            for page in dash.page_registry.values()
        ]),

        # content of each page
        html.Div(id='page-content')
    ]
)

@app.callback(
    Output('page-content', 'children'),
    [Input('tabs-example', 'value')]
)
def display_page(pathname):
    selected_page = next((page for page in dash.page_registry.values() if page['path'] == pathname), None)

    if selected_page:
        return selected_page['layout']
    else:
        return html.Div("Page not found")

if __name__ == "__main__":
    app.run(debug=True)