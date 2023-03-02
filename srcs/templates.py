# srcs/streamlit_app/templates.py
def search_result(i: int, url: str, title: str, content: str, sim: float) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {i + 1}.
            <a href="{url}" target="_blank">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                Similaridade de {sim:.2f}%
            </div>
        </div>
    """
