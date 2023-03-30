import boilerplate.config as config
from boilerplate.db import db
from flask import Flask
from sqlalchemy.exc import OperationalError

# ==============================================================================================================================================================
#                                                                      Configuration
# ==============================================================================================================================================================
# Setup Flask app object
app = Flask(__name__)
app.secret_key = config.APP_SECRET
app.debug = config.DEBUG_MODE

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==============================================================================================================================================================
#                                                                   App Initialization
# ==============================================================================================================================================================
db.init_app(app)
with app.app_context():
    # Import all app modules
    import boilerplate.errors
    import boilerplate.utils.filters
    import boilerplate.modules.role as role
    import boilerplate.modules.user
    import boilerplate.modules.login

    # Create any db models
    db.create_all()
    db.session.commit()

    # Run the database initialization seeding tasks if needed
    #role.role_model.seed_roles_if_required()
    role.role_model.update_system_roles()
    #role.role_model.action_clean_up()
    #user.user_model.seed_user_if_required()

