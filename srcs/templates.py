# srcs/streamlit_app/templates.py
def search_result(i: int, url: str, title: str, content: str, sim: float) -> str:
    """ HTML scripts to display search results. """
    section_template = get_section_template(i, url, title, content)
    return f"""
        {section_template}
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                Similaridade de {sim:.2f}%
            </div>
        </div>
    """

def get_section_template(index: int, url: str, title: str, content: str) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {index + 1}.
            <a href="{url}" target="_blank">
                {title}
            </a>
        </div>
    """
