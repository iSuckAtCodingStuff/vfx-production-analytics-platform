from dash import dash_table


def create_report_table(component_id: str):
    """ Create a reusable Dash DataTable for analytical reports.
    Args:
        component_id: Dash DataTable component ID.
    Returns:
        Configured Dash DataTable""" 
    
    return dash_table.DataTable(
        id=component_id,
        page_size=10,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto", "marginTop": "40px"},
        style_cell={"textAlign": "left", "padding": "10px"},
        style_header={"fontWeight": "bold"}
    )