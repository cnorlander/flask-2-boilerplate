from flask import Flask
import time, asyncio, os
import boilerplate.config as config
from boilerplate.app import app
import boilerplate.modules.user.user_controller

__author__ = "Corey Norlander"
__copyright__ = "Copyright 2023, Corey Norlander"
__credits__ = ["Corey Norlander"]
__version__ = "0.0.1"
__email__ = "corey@flaresoftworks.com"

# set timezone
os.environ['TZ'] = config.TIMEZONE
time.tzset()


@app.route('/')
async def hello_world():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return f"<h1>{current_time}</h1>"