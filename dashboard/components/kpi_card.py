from dash import html


def create_kpi_card(title: str, component_id: str):
    return html.Div(
        [
            html.H4(title, className="kpi-title"),
            html.H2("...", id=component_id, className="kpi-value")
        ],
        className="kpi-card"
    )