from flask_sqlalchemy import abort
from app import db
from flask import make_response
from app.models.customer import Customer
from app.models.video import Video

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

def valid_input(request_body, model):
    if model == Customer:
        if "name" not in request_body:
            abort(make_response({"details": f"Request body must include name."}, 400))
        if "phone" not in request_body:
            abort(make_response({"details": f"Request body must include phone."}, 400))
        if "postal_code" not in request_body:
            abort(make_response({"details": f"Request body must include postal_code."}, 400))
    if model == Video:
        if "title" not in request_body:
            abort(make_response({"details": f"Request body must include title."}, 400))
        if "release_date" not in request_body:
            abort(make_response({"details": f"Request body must include release_date."}, 400))
        if "total_inventory" not in request_body:
            abort(make_response({"details": f"Request body must include total_inventory."}, 400))

def add_to_database(model_instance):
    """Adds valid instance of a model to database"""
    db.session.add(model_instance)
    db.session.commit()

def delete_from_database(model_instance):
    """Deletes valid instance of a model from detabase"""
    db.session.delete(model_instance)
    db.session.commit()



