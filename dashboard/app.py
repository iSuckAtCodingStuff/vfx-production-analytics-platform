from dash import Dash, html, page_container

from dashboard.callbacks import register_callbacks
from dashboard.components.footer import create_footer
from dashboard.components.navbar import create_navbar

#==========================================================================
# Initialize the Dash application
#==========================================================================
app = Dash(__name__, use_pages=True,
    suppress_callback_exceptions=True,
    title="VFX Production Analytics Dashboard"
)
server = app.server

register_callbacks(app)

#==========================================================================
# Root layout
#==========================================================================
app.layout = html.Div(
    [
        create_navbar(),
        page_container,
        create_footer()
    ]
)


if __name__ == "__main__":
    app.run(debug=True)