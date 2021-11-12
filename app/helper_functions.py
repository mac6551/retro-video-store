from flask_sqlalchemy import abort
from app import db

def valid_id(model, id):
    """Returns instance of model with matching ID."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})
    return model.query.get(id)

def add_to_database(model_instance):
    """Adds valid instance of a model to database"""
    db.session.add(model_instance)
    db.session.commit()

def delete_from_database(model_instance):
    """Deletes valid instance of a model from detabase"""
    db.session.delete(model_instance)
    db.session.commit()



