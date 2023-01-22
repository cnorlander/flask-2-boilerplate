import boilerplate.config as config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Setup Flask app object
app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.debug = config.DEBUG_MODE

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()