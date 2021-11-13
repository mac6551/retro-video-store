from flask_sqlalchemy import abort
from app import db
from flask import make_response

def valid_id(model, id, model_string):
    """ Parameters: Model, id of item, and string version of model name.
        Returns instance of model with matching ID.
        Returns 404 and custom messgae if model with given ID does not exist."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})

    model = model.query.get(id)
    model_string = str(model_string).capitalize()

    if not model: 
        abort(make_response({"message": f"{model_string} {id} was not found"}, 404))

    return model


def add_to_database(model_instance):
    """Adds valid instance of a model to database"""
    db.session.add(model_instance)
    db.session.commit()

def delete_from_database(model_instance):
    """Deletes valid instance of a model from detabase"""
    db.session.delete(model_instance)
    db.session.commit()



