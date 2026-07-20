from dash import html, register_page

from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_container import create_chart_container
from dashboard.components.report_table import create_report_table


register_page(__name__, path="/renders", name="Renders")

layout = html.Div(className="page-container", children=[

        html.H1("Render Dashboard", className="page-title"),

        html.Div(className="kpi-grid", children=[
                create_kpi_card("Successful Renders", "render-successful"),
                create_kpi_card("Failed Renders", "render-failed"),
                create_kpi_card("Success Rate", "render-success-rate"),
                create_kpi_card("Total Render Jobs", "render-total-jobs"),
            ],
        ),

        create_chart_container("render-status-chart"),

        create_chart_container("render-hours-chart"),

        html.H2("Render Hours by Project"),

        create_report_table("render-table"),
    ],
)