from boilerplate.app import app
from titlecase import titlecase

@app.template_filter()
def deunderscore_title(string):
    return titlecase(string.replace("_", " "))