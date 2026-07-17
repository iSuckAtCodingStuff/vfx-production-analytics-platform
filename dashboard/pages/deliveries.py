from dash import html, register_page

register_page(__name__, path="/deliveries", name="Deliveries", title="Deliveries")

layout = html.Div(
    [
        html.H2("Deliveries"),
        html.P("Delivery metrics will appear here.")
    ],
    className="page-content")