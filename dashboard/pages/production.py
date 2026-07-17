from dash import html, register_page

register_page(__name__, path="/production", name="Production", title="Production")

layout = html.Div(
    [
        html.H2("Production"),
        html.P("Production metrics will appear here.")
    ],
    className="page-content")
