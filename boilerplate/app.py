from flask import Flask
import boilerplate.config as config

app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.debug = config.DEBUG_MODE
