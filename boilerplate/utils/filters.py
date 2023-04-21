from boilerplate.app import app
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