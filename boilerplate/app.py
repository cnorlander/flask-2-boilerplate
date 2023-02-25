import boilerplate.config as config
from boilerplate.db import db
from flask import Flask
from sqlalchemy.exc import OperationalError


# Setup Flask app object
app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.debug = config.DEBUG_MODE

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
with app.app_context():
    import boilerplate.modules.user.user_controller
    import boilerplate.modules.login.login_controller
    import boilerplate.modules.role.role_controller
    import boilerplate.modules.user.user_model
    import boilerplate.modules.role.role_model

    db.create_all()
    db.session.commit()


    boilerplate.modules.role.role_model.seed_roles_if_required()
    boilerplate.modules.role.role_model.update_system_roles()
   # boilerplate.modules.role.role_model.action_clean_up()
    boilerplate.modules.user.user_model.seed_user_if_required()

