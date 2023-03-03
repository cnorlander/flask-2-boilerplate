from boilerplate.app import app
from flask import render_template, abort
import base64
import uuid

#TODO: Add logging to all these errors
@app.errorhandler(400)
def bad_request(error, debug=None, detailed_message=None):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 400
    message = "Bad Request. Something was wrong with the data you submitted to the server. " \
              "Please Try Again. If this error continues to occur please report this error."
    message = detailed_message if detailed_message else message
    return render_template('error.html', http_status_code=http_status_code, error=str(error), debug=debug, message=message, error_id=error_id), http_status_code

@app.errorhandler(403)
def forbidden(error, debug=None, detailed_message=None):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 403
    message = "Forbidden. You do not have permission to perform this action."
    message = detailed_message if detailed_message else message
    return render_template('error.html', http_status_code=http_status_code, error=str(error), debug=debug, message=message, error_id=error_id), http_status_code

@app.errorhandler(404)
def page_not_found(error, debug=None, detailed_message=None):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 404
    message = "Not Found. The resource you requested could not be found. " \
              "Please Try Again. If this error continues to occur please report this error."
    message = detailed_message if detailed_message else message
    return render_template('error.html', http_status_code=http_status_code, error=str(error), debug=debug, message=message, error_id=error_id), http_status_code

@app.errorhandler(500)
def internal_server_error(error, debug=None, detailed_message=None):
    error_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").strip("==")
    http_status_code = 500
    message = "Internal Server Error. Something went wrong and the server could not recover. " \
              "Please Try Again. If this error continues to occur please report this error."
    message = detailed_message if detailed_message else message
    return render_template('error.html', http_status_code=http_status_code, error=str(error), debug=debug, message=message, error_id=error_id), http_status_code

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

