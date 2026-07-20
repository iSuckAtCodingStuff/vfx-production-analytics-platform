from dash import html, dcc, page_registry


def create_navbar() -> html.Nav:
    """ Create the application's navigation bar.
    Returns:
        Dash HTML navigation component """
    
    links = []

    for page in page_registry.values():
        links.append(dcc.Link(page["name"], href=page["relative_path"]))

    return html.Nav(
        [
            html.H1("VFX Production Analytics Dashboard"),

            html.P("Production Analytics & Business Intelligence"),

            html.Div(links, className="nav-links")
        ],
        className="navbar"
    )