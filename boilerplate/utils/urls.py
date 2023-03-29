from boilerplate.app import app
from urllib.parse import urlparse, urljoin, unquote
from flask import request, url_for
import importlib

def is_safe_url(target: str):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def route_info():
    routes = []
    # Fetch data about all the routes
    for rule in app.url_map.iter_rules():
        view_function = app.view_functions[rule.endpoint]
        module = view_function.__module__
        #location = view_function.__module__['__file__']
        location = str(importlib.util.find_spec(module).origin)
        method = list(rule.methods)

        # Format the url options parameters
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        url = unquote(url_for(rule.endpoint, **options))

        # Check to see if the function requires auth
        auth_required = False
        if 'is_authenticated' in view_function.__code__.co_names:
            auth_required = True

        # create a dictionary object to represent the route and add it to the routes list
        route = {'method': method, 'url': url, 'auth_required': auth_required, 'location': location, 'module': module}
        routes.append(route)
    return routes