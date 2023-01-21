from flask import Flask
import time, asyncio, os
import boilerplate.config as config

# set timezone
os.environ['TZ'] = config.TIMEZONE
time.tzset()

app = Flask(__name__)


@app.route('/')
async def hello_world():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return f'<h1>{current_time}</h1>'