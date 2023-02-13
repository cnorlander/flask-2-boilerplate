from flask import Flask, redirect, url_for
import time, asyncio, os
import boilerplate.config as config
from boilerplate.app import app
from flask_login import login_required
import boilerplate.modules.user.user_controller
import boilerplate.modules.login.login_controller

__author__ = "Corey Norlander"
__copyright__ = "Copyright 2023, Corey Norlander"
__credits__ = ["Corey Norlander"]
__version__ = "0.0.1"
__email__ = "corey@flaresoftworks.com"

# set timezone
os.environ['TZ'] = config.TIMEZONE
time.tzset()


@app.route('/')
@login_required
def index():
    return redirect(url_for("get_user_list"))