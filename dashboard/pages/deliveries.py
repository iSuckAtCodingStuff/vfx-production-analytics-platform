from dash import html, register_page

from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_container import create_chart_container
from dashboard.components.report_table import create_report_table

register_page(__name__, path="/deliveries", name="Deliveries")

layout = html.Div(className="page-container", children=[

        html.H1("Deliveries Dashboard", className="page-title"),

        html.Div(className="kpi-grid", children=[
                create_kpi_card("Approved", "delivery-approved"),
                create_kpi_card("Rejected", "delivery-rejected"),
                create_kpi_card("Approval Rate", "delivery-approval-rate"),
                create_kpi_card("Total Deliveries", "delivery-total"),
            ],
        ),

        create_chart_container("delivery-status-chart"),

        create_chart_container("delivery-project-chart"),

        html.H2("Deliveries by Project"),

        create_report_table("delivery-table"),
    ],
)