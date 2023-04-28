from boilerplate.app import app
from boilerplate.config import NUMBER_OF_PROFILE_COLORS
from titlecase import titlecase

@app.template_filter()
def deunderscore_title(string):
    return titlecase(string.replace("_", " "))

@app.template_filter()
def tuple_to_simple_list(items):
    string = ""
    for item in items:
        string += f'{str(item)}, '
    if len(string) > 0:
        string = string[:-2]
    return string

@app.template_filter()
def profile_color_id(user_id: int):
    mapped_id = user_id % NUMBER_OF_PROFILE_COLORS
    if mapped_id == NUMBER_OF_PROFILE_COLORS:
        return NUMBER_OF_PROFILE_COLORS
    return mapped_id
