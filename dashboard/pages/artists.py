from dash import html, register_page

register_page(__name__, path="/artists", name="Artists",title="Artists")

layout = html.Div(
    [
        html.H2("Artists"),
        html.P("Artist analytics will appear here.")
    ],
    className="page-content")