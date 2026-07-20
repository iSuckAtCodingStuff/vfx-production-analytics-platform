from dash import html


def create_footer()-> html.Footer:
    """ Create the dashboard footer.
    Returns:
        Dash HTML footer component """
    
    return html.Footer([html.P("VFX Production Analytics Platform")], className="footer")