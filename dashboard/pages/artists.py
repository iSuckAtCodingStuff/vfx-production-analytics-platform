from dash import html, dcc, register_page

from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.report_table import create_report_table
from dashboard.components.chart_container import create_chart_container

register_page(__name__, path="/artists", name="Artists")

layout = html.Div(className="page-container", children=[
        html.H1("Artists Dashboard", className="page-title"),

        # =====================================================
        # KPI Cards
        # =====================================================

        html.Div(className="kpi-grid", children=[
                create_kpi_card("Departments", "artists-total-departments"),
                create_kpi_card("Total Artists", "artists-total-artists"),
                create_kpi_card("Hours Logged", "artists-total-hours"),
                create_kpi_card("Avg Hours / Artist", "artists-average-hours"),
                create_kpi_card("Largest Department", "artists-largest-department"),
            ]
        ),

        # =====================================================
        # Chart
        # =====================================================
        
        create_chart_container("artists-utilization-chart"),
                
        # =====================================================
        # Table
        # =====================================================

        create_report_table("artists-table")
    ]
)