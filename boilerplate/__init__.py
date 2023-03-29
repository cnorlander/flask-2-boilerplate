import time, asyncio, os
import boilerplate.config as config
from flask import Flask, redirect, url_for, abort
from boilerplate.app import app
from flask_login import login_required, current_user
from boilerplate.utils.urls import route_info


__author__ = "Corey Norlander"
__copyright__ = "Copyright 2023, Corey Norlander"
__credits__ = ["Corey Norlander"]
__version__ = "0.0.1"
__email__ = "corey@flaresoftworks.com"

# set timezone
os.environ['TZ'] = config.TIMEZONE
time.tzset()


@app.route('/')
def index():
    return redirect(url_for("get_user_list"))

@app.get('/api/v1/routes')
@login_required
def get_all_routes():
    if current_user.role.system:
        return route_info()
    return abort(403)
