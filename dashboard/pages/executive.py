from dash import html, register_page

from dashboard.components.kpi_card import create_kpi_card

#==========================================================================
# Register this page with Dash
#==========================================================================
register_page(__name__, path="/", name="Executive Overview", title="Executive Overview")


layout = html.Div(
    [
        html.H2("Executive Overview"),
        html.P("High-level production KPIs and project summary."),
        html.Div(
            [
                create_kpi_card("Total Projects","total-projects"),
                create_kpi_card("Active Projects", "active-projects"),
                create_kpi_card("Artists", "total-artists"),
                create_kpi_card("Deliveries", "total-deliveries")
            ],
            className="kpi-grid"
        )
    ],
    className="page-content"
)