import time, asyncio, os
import boilerplate.config as config
from boilerplate.app import app
from flask import Flask, redirect, url_for, abort
from flask_login import login_required, current_user
from boilerplate.utils.urls import route_info
from boilerplate.modules.role.role_decorators import require_system_role


# ==============================================================================================================================================================
#                                                                      Configuration
# ==============================================================================================================================================================
__author__ = "Corey Norlander"
__copyright__ = "Copyright 2023, Corey Norlander"
__credits__ = ["Corey Norlander"]
__version__ = "0.0.1"
__email__ = "corey@flaresoftworks.com"

# set timezone
os.environ['TZ'] = config.TIMEZONE
time.tzset()

# ==============================================================================================================================================================
#                                                                      View Routes
# ==============================================================================================================================================================
@app.route('/')
def index():
    return redirect(url_for("get_user_list"))

# ==============================================================================================================================================================
#                                                                    Endpoint Routes
# ==============================================================================================================================================================
@app.get('/api/v1/routes')
@login_required
@require_system_role
def get_all_routes():
    return sorted(route_info(), key=lambda route: route['module'])

