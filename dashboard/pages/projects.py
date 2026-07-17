from dash import html, register_page

register_page(__name__, path="/projects", name="Projects", title="Projects")

layout = html.Div(
    [
        html.H2("Projects"),
        html.P("Project metrics will appear here.")
    ],
    className="page-content")