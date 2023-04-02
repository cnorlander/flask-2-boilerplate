from boilerplate.app import app
import boilerplate.utils.lumberjack as log
from flask import render_template, abort, request
from flask_login import current_user
from datetime import datetime
import boilerplate.config as config
import base64
import uuid
import traceback

def get_request_body_string(error_request):
    try:
        # Try to get the JSON data
        json_data = error_request.get_json()
        if json_data is not None:
            return str(json_data)
    except:
        pass

    try:
        # Try to get the form data
        form_data = error_request.form
        if len(form_data) > 0:
            return str(form_data.to_dict(flat=False))
    except:
        pass

    # If we couldn't retrieve the JSON or form data, just return the raw request body
    return str(error_request.data)

# ==============================================================================================================================================================
#                                                                   Error Views
# ==============================================================================================================================================================
#TODO: Add logging to all these errors
@app.errorhandler(400)
def bad_request(error):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 400
    message = "Bad Request. Something was wrong with the data you submitted to the server. " \
              "Please Try Again. If this error continues to occur please report this error."
    if error.description:
        message = error.description

    # Log if required
    if config.LOGGING_LOG_400_ERRORS:
        user = "Anonymous" if current_user.get_id() is None else current_user.get_id()
        log.error(f'HTTP {http_status_code} ({error_id}) {request.method}:{request.url} BY:({user})- {message}')
        if request.method != "GET":
            body_data = get_request_body_string(request)
            log.debug(f"Body Data ({error_id}):\r\n {body_data}")

    return render_template('error.html', http_status_code=http_status_code, error=str(error), message=message, error_id=error_id, now=datetime.now()), http_status_code

@app.errorhandler(403)
def forbidden(error):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 403
    message = "Forbidden. You do not have permission to perform this action."
    print("Description: ", error.description, flush=True)
    if error.description:
        message = error.description

    # Log if required
    if config.LOGGING_LOG_403_ERRORS:
        user = "Anonymous" if current_user.get_id() is None else current_user.get_id()
        log.error(f'HTTP {http_status_code} ({error_id}) {request.method}:{request.url} BY:({user})- {message}')
        if request.method != "GET":
            body_data = get_request_body_string(request)
            log.debug(f"Body Data ({error_id}):\r\n {body_data}")

    return render_template('error.html', http_status_code=http_status_code, error=str(error), message=message, error_id=error_id, now=datetime.now()), http_status_code

@app.errorhandler(404)
def page_not_found(error):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 404
    message = "Not Found. The resource you requested could not be found. " \
              "Please Try Again. If this error continues to occur please report this error."
    if error.description:
        message = error.description

    # Log if required
    if config.LOGGING_LOG_404_ERRORS:
        user = "Anonymous" if current_user.get_id() is None else current_user.get_id()
        log.error(f'HTTP {http_status_code} ({error_id}) {request.method}:{request.url} BY:({user})- {message}')
        if request.method != "GET":
            body_data = get_request_body_string(request)
            log.debug(f"Body Data ({error_id}):\r\n {body_data}")

    return render_template('error.html', http_status_code=http_status_code, error=str(error), message=message, error_id=error_id, now=datetime.now()), http_status_code

@app.errorhandler(500)
def internal_server_error(error):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 500
    message = "Internal Server Error. Something went wrong and the server could not recover. " \
              "Please Try Again. If this error continues to occur please report this error."
    if error.description:
        message = error.description

    # Log if required
    if config.LOGGING_LOG_500_ERRORS:
        exception_traceback = False
        if error.original_exception:
            exception_traceback = traceback.format_exc()
        user = "Anonymous" if current_user.get_id() is None else current_user.get_id()
        log.error(f'HTTP {http_status_code} ({error_id}) {request.method}:{request.url} BY:({user})- {message}', traceback=exception_traceback)
        if request.method != "GET":
            body_data = get_request_body_string(request)
            log.debug(f"Body Data ({error_id}):\r\n {body_data}")

    return render_template('error.html', http_status_code=http_status_code, error=str(error), message=message, error_id=error_id, now=datetime.now()), http_status_code

# ==============================================================================================================================================================
#                                                                Error Views Test Routes
# ==============================================================================================================================================================
@app.get("/errors/400")
def error_test_400():
    return abort(400)

@app.get("/errors/403")
def error_test_403():
    return abort(403)

@app.get("/errors/404")
def error_test_404():
    return abort(404)

@app.get("/errors/500")
def error_test_500():
    return abort(500)

@app.get("/errors/div0")
def error_div0():
    test = 5/0
    return "We will never get here"

@app.post("/errors/post")
def post_test():
    return abort(400)

