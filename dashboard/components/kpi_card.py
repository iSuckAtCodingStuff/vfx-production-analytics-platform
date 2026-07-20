from dash import html


def create_kpi_card(title: str, component_id: str)-> html.Div:
    """ Create a reusable KPI card component.
    Args:
        title: KPI title displayed on the card.
        component_id: Dash component ID used for callback updates.
    Returns:
        Dash HTML Div containing the KPI card """

    return html.Div(
        [
            html.H4(title, className="kpi-title"),
            html.H2("...", id=component_id, className="kpi-value")
        ],
        className="kpi-card"
    )