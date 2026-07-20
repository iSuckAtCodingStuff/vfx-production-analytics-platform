from dash import html, dcc


def create_chart_container(component_id: str)-> html.Div:
    """Create a reusable container for Plotly charts.
    Args:
        component_id: Dash Graph component ID.
    Returns:
        Styled Dash HTML Div containing a Graph component """
    
    return html.Div(className="chart-card", children=[dcc.Graph(id=component_id)])