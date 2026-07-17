from dash import Input, Output

from dashboard.query_runner import execute_scalar


def register_callbacks(app):
    @app.callback(Output("total-projects", "children"), Input("total-projects", "id"))
    
    def load_total_projects(_):
        value = execute_scalar("project_metrics/total_projects.sql")

        return f"{value:,}"

    @app.callback(Output("active-projects", "children"), Input("active-projects", "id"))
    
    def load_active_projects(_):

        return "Coming Soon"

    @app.callback(
        Output("total-artists", "children"),

        Input("total-artists", "id")

    )
    def load_total_artists(_):

        return "Coming Soon"

    @app.callback(

        Output("total-deliveries", "children"),

        Input("total-deliveries", "id")

    )
    def load_total_deliveries(_):

        return "Coming Soon"