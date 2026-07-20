from dash import Input, Output

import plotly.express as px

from dashboard.query_runner import execute_sql
from dashboard.components.chart_container import create_chart_container


# =====================================================
# Shared Helper Functions
# =====================================================

def apply_chart_theme(fig):

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(x=0.5, xanchor="center", font=dict(size=18)),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(size=13)
    )

    return fig

# =====================================================
# Executive Chart Helpers
# =====================================================

def create_project_status_chart(df) -> Figure:

    status_df = (df.groupby("project_status").size().reset_index(name="count"))

    fig = px.pie(status_df, names="project_status", values="count", hole=0.6, title="Projects by Status")

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>"
                      "Projects: %{value}<br>"
                      "Percentage: %{percent}<extra></extra>"
    )

    return apply_chart_theme(fig)


def create_project_type_chart(df) -> Figure:

    type_df = (df.groupby("project_type").size().reset_index(name="count"))

    fig = px.pie(type_df, names="project_type", values="count", hole=0.6, title="Projects by Type")

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>"
                      "Projects: %{value}<br>"
                      "Percentage: %{percent}<extra></extra>"
    )

    return apply_chart_theme(fig)



def create_budget_chart(df) -> Figure:

    budget_df = df.sort_values("budget_million_usd", ascending=True)

    fig = px.bar(budget_df, x="budget_million_usd", y="project_name", orientation="h", title="Budget by Project")

    fig.update_traces(
        texttemplate="$%{x:.1f}M",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>"
                      "Budget: $%{x:.1f}M<extra></extra>"
    )

    fig.update_xaxes(tickprefix="$", ticksuffix="M", showgrid=False)

    fig.update_yaxes(showgrid=False)

    return apply_chart_theme(fig)


def create_task_completion_chart(df) -> Figure:

    completion_df = df.sort_values("task_completion_pct", ascending=True)

    fig = px.bar(completion_df, x="task_completion_pct", y="project_name", orientation="h", title="Task Completion (%)")

    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>"
                      "Completion: %{x:.1f}%<extra></extra>"
    )

    fig.update_xaxes(ticksuffix="%", showgrid=False)

    fig.update_yaxes(showgrid=False)

    return apply_chart_theme(fig)


# =====================================================
# Projects Chart Helpers
# =====================================================

def create_project_resource_chart(df) -> Figure:

    chart_df = df.sort_values("total_hours_logged", ascending=True)

    fig = px.bar(chart_df, x="total_hours_logged", y="project_name", orientation="h", title="Hours Logged by Project")

    fig.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>"
                      "Hours Logged: %{x:,.2f}<extra></extra>"
    )

    fig.update_xaxes(title="Hours Logged", showgrid=False)

    fig.update_yaxes(title=None, showgrid=False)

    return apply_chart_theme(fig)


# =====================================================
# Artists Chart Helpers
# =====================================================

def create_department_utilization_chart(df) -> Figure:

    chart_df = df.sort_values("total_hours_logged", ascending=True)

    fig = px.bar(chart_df, x="total_hours_logged", y="department", orientation="h", title="Department Utilization")

    fig.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>"
                      "Hours Logged: %{x:,.2f}<extra></extra>"
    )

    fig.update_xaxes(title="Hours Logged", showgrid=False)

    fig.update_yaxes(title=None, showgrid=False)

    return apply_chart_theme(fig)


# =====================================================
# Render Chart Helpers
# =====================================================

def create_render_status_chart(df) -> Figure:

    fig = px.pie(
        df,
        names="render_status",
        values="total_render_jobs",
        title="Render Job Status Distribution",
    )

    return fig

def create_render_hours_chart(df):

    fig = px.bar(
        df,
        x="project_name",
        y="total_render_hours",
        title="Render Hours by Project",
        text="total_render_hours",
    )

    fig.update_layout(xaxis_title="Project", yaxis_title="Render Hours",)

    return fig


# =====================================================
# Render Chart Helpers
# =====================================================

def create_delivery_status_chart(df) -> Figure:

    fig = px.pie(
        df,
        names="client_status",
        values="total_deliveries",
        title="Delivery Approval Status",
        color="client_status",
        color_discrete_map={
            "Approved": "blue",
            "Rejected": "red",
        }
    )

    return fig

def create_deliveries_project_chart(df) -> Figure:

    fig = px.bar(
        df,
        x="project_name",
        y="total_deliveries",
        title="Deliveries by Project",
        text="total_deliveries",
    )

    fig.update_layout(xaxis_title="Project", yaxis_title="Total Deliveries",)

    return fig

# =====================================================
# Register Callbacks
# =====================================================

def register_callbacks(app: Dash)-> None:

    """ Register all dashboard callbacks.
    Args:
        app: Dash application instance.
    Returns:
        None """
    # --------------------------------------
    # Executive KPI Callback
    # --------------------------------------
    @app.callback(
        Output("kpi-total-projects", "children"),
        Output("kpi-total-artists", "children"),
        Output("kpi-total-sequences", "children"),
        Output("kpi-total-shots", "children"),
        Output("kpi-total-tasks", "children"),
        Output("kpi-total-hours", "children"),
        Output("kpi-render-hours", "children"),
        Output("kpi-total-deliveries", "children"),
        Output("kpi-approval-rate", "children"),
        Output("kpi-render-success", "children"),
        Input("url", "pathname"),
    )
    def load_executive_dashboard(_):

        df = execute_sql("executive_dashboard/40_studio_kpi_dashboard.sql")

        row = df.iloc[0]

        return (
            f"{row['total_projects']:,}",
            f"{row['total_artists']:,}",
            f"{row['total_sequences']:,}",
            f"{row['total_shots']:,}",
            f"{row['total_tasks']:,}",
            f"{row['total_hours_logged']:,.2f}",
            f"{row['total_render_hours']:,.2f}",
            f"{row['total_deliveries']:,}",
            f"{row['approval_rate']:.2f}%",
            f"{row['render_success_rate']:.2f}%"
        )
    
    # --------------------------------------
    # Executive Charts Callback
    # --------------------------------------
    @app.callback(
        Output("project-status-chart", "figure"),
        Output("project-type-chart", "figure"),
        Output("budget-chart", "figure"),
        Output("task-completion-chart", "figure"),
        Input("url", "pathname"),
    )
    
    def load_executive_charts(_):

        df = execute_sql("executive_dashboard/41_project_health_dashboard.sql")

        return (
            create_project_status_chart(df),
            create_project_type_chart(df),
            create_budget_chart(df),
            create_task_completion_chart(df)
        )
  
    # --------------------------------------
    # Project KPI Callback
    # --------------------------------------

    @app.callback(
        Output("projects-total-projects", "children"),
        Output("projects-total-tasks", "children"),
        Output("projects-total-hours", "children"),
        Output("projects-render-hours", "children"),
        Output("projects-total-deliveries", "children"),
        Output("projects-resource-chart", "figure"),
        Output("projects-table", "data"),
        Output("projects-table", "columns"),
        Input("url", "pathname")
    )

    def load_projects_dashboard(_):
        
        df = execute_sql("project_metrics/07_project_resource_summary.sql")
        
        total_projects = len(df)
        
        total_tasks = df["total_tasks"].sum()
        
        total_hours = df["total_hours_logged"].sum()
        
        render_hours = df["total_render_hours"].sum()
        
        deliveries = df["total_deliveries"].sum()

        chart_df = df.sort_values("total_hours_logged", ascending=True)

        fig = create_project_resource_chart(df)

        return (
            f"{total_projects:,}",

            f"{total_tasks:,}",

            f"{total_hours:,.2f}",

            f"{render_hours:,.2f}",

            f"{deliveries:,}",

            fig,

            df.to_dict("records"),

            [{"name": c.replace("_", " ").title(), "id": c} for c in df.columns]
        )
    

# --------------------------------------
# Artists Dashboard Callback
# --------------------------------------

    @app.callback(

        Output("artists-total-departments", "children"),
        Output("artists-total-artists", "children"),
        Output("artists-total-hours", "children"),
        Output("artists-average-hours", "children"),
        Output("artists-largest-department", "children"),

        Output("artists-utilization-chart", "figure"),

        Output("artists-table", "data"),
        Output("artists-table", "columns"),

        Input("url", "pathname")

    )
    def load_artists_dashboard(_):

        df = execute_sql("artist_metrics/21_department_utilization.sql")

        total_departments = len(df)

        total_artists = df["total_artists"].sum()

        total_hours = df["total_hours_logged"].sum()

        average_hours = total_hours / total_artists

        largest_department = df.loc[df["total_artists"].idxmax(),"department"]

        fig = create_department_utilization_chart(df)

        return (

            f"{total_departments:,}",

            f"{total_artists:,}",

            f"{total_hours:,.2f}",

            f"{average_hours:,.2f}",

            largest_department,

            fig,

            df.to_dict("records"),[{"name": c.replace("_", " ").title(),"id": c}for c in df.columns]
        )
    
# --------------------------------------
# Renders Dashboard Callback
# --------------------------------------

    @app.callback(
    Output("render-successful", "children"),
    Output("render-failed", "children"),
    Output("render-success-rate", "children"),
    Output("render-total-jobs", "children"),
    Output("render-status-chart", "figure"), 
    Output("render-hours-chart", "figure"),
    Output("render-table", "data"),
    Output("render-table", "columns"),
    Input("url", "pathname"),
    )

    def update_render_dashboard(_):

        success_df = execute_sql("render_metrics/32_render_success_rate.sql")

        hours_df = execute_sql("render_metrics/35_render_hours_by_project.sql")

        successful = success_df.loc[success_df["render_status"] == "Success", "total_render_jobs"].iloc[0]
        
        failed = success_df.loc[success_df["render_status"] == "Failed", "total_render_jobs"].iloc[0]
        
        success_rate = success_df.loc[success_df["render_status"] == "Success", "percentage"].iloc[0]

        total_jobs = success_df["total_render_jobs"].sum()

        status_figure = create_render_status_chart(success_df)

        hours_figure = create_render_hours_chart(hours_df)

        return (
            f"{successful:,}",
            f"{failed:,}",
            f"{success_rate:.1f}%",
            f"{total_jobs:}",
            status_figure,
            hours_figure,
            hours_df.to_dict("records"),
            [{"name": c, "id": c} for c in hours_df.columns],
        )
    

# --------------------------------------
# Deliveries Dashboard Callback
# --------------------------------------

    @app.callback(
    Output("delivery-approved", "children"),
    Output("delivery-rejected", "children"),
    Output("delivery-approval-rate", "children"),
    Output("delivery-total", "children"),
    Output("delivery-status-chart", "figure"),
    Output("delivery-project-chart", "figure"),
    Output("delivery-table", "data"),
    Output("delivery-table", "columns"),
    Input("url", "pathname"),
    )
    def update_delivery_dashboard(_):

        status_df = execute_sql("delivery_metrics/37_delivery_approval_rate.sql")

        project_df = execute_sql("delivery_metrics/39_deliveries_by_project.sql")

        approved = status_df.loc[
            status_df["client_status"] == "Approved",
            "total_deliveries"
        ].iloc[0]

        rejected = status_df.loc[
            status_df["client_status"] == "Rejected",
            "total_deliveries"
        ].iloc[0]

        approval_rate = status_df.loc[
            status_df["client_status"] == "Approved",
            "percentage"
        ].iloc[0]

        total = status_df["total_deliveries"].sum()

        status_chart = create_delivery_status_chart(status_df)

        project_chart = create_deliveries_project_chart(project_df)

        return (
            f"{approved:,}",
            f"{rejected:,}",
            f"{approval_rate:.1f}%",
            f"{total:,}",
            status_chart,
            project_chart,
            project_df.to_dict("records"),
            [{"name": c, "id": c} for c in project_df.columns],
        )