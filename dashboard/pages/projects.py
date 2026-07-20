from dash import html, dcc, register_page

from dashboard.components.report_table import create_report_table
from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_container import create_chart_container

register_page(__name__, path="/projects", name="Projects")

layout = html.Div(className="page-container", children=[
        html.H1("Projects Dashboard", className="page-title"),

        # =====================================================
        # KPI Cards
        # =====================================================

        html.Div(className="kpi-grid", children=[
                create_kpi_card("Total Projects", "projects-total-projects"),
                create_kpi_card("Total Tasks", "projects-total-tasks"),
                create_kpi_card("Hours Logged", "projects-total-hours"),
                create_kpi_card("Render Hours", "projects-render-hours"),
                create_kpi_card("Total Deliveries", "projects-total-deliveries"),
            ]
        ),

        # =====================================================
        # Chart
        # =====================================================

        create_chart_container("projects-resource-chart"),

        # =====================================================
        # Report Table
        # =====================================================

        create_report_table("projects-table")
    ]
)