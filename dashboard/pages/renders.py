from dash import html, register_page

register_page(__name__, path="/renders", name="Renders", title="Render Analytics")

layout = html.Div(
    [
        html.H2("Render Analytics"),
        html.P("Render metrics will appear here.")
    ],
    className="page-content")