from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def save():
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
    return True
