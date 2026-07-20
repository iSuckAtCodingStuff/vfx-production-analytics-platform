from dash import html, dcc, register_page

from dashboard.components.kpi_card import create_kpi_card
from dashboard.components.chart_container import create_chart_container

register_page(__name__, path="/", name="Executive")

layout = html.Div(className="page-container", children=[html.H1("Executive Dashboard", className="page-title"),

        # ==========================
        # KPI Section
        # ==========================

        html.Div(className="kpi-grid", children=[

        create_kpi_card(title="Total Projects", component_id="kpi-total-projects"),

        create_kpi_card(title="Total Artists", component_id="kpi-total-artists"),

        create_kpi_card(title="Total Sequences", component_id="kpi-total-sequences"),

        create_kpi_card(title="Total Shots", component_id="kpi-total-shots"),

        create_kpi_card(title="Total Tasks", component_id="kpi-total-tasks"),

        create_kpi_card(title="Hours Logged", component_id="kpi-total-hours"),

        create_kpi_card(title="Render Hours", component_id="kpi-render-hours" ),

        create_kpi_card(title="Total Deliveries", component_id="kpi-total-deliveries"),

        create_kpi_card(title="Approval Rate", component_id="kpi-approval-rate"),

        create_kpi_card(title="Render Success Rate",component_id="kpi-render-success"),
    ]
),

        # ==========================
        # Charts
        # ==========================

        create_chart_container("project-status-chart"),
        create_chart_container("project-type-chart"),
        create_chart_container("budget-chart"),
        create_chart_container("task-completion-chart"),
    ]
)