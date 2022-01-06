import os


def add_title(file, title=None):
    """
    Take a HTML file and add a <h1> tag to the top of the file. 
    The <h1> tag will be centered between two dashed lines. One on the left and one on the right.
    
    Returns:
        - <str> The file with the title added.
    """
    if title is None:
        # Use the file name
        title = os.path.basename(file)
    
    dash_color = "#9fa8da"
    html = f"""
    <div style="align-items: center;">
        <h3 style="text-align: center; color: white; margin-bottom: 0;"> {title} </h3>
        <hr style="padding: 7px; margin-top: 0; background-color: {dash_color}; border: none; border-radius: 20px; width: 10%;" />
    </div>
    """

    # Open the file and add to the first line of the file
    with open(file, "r", encoding="utf8") as r_file:
        # Get the file contents
        contents = r_file.read()
        # Add the html to the top of the file
        contents = html + contents
        return contents