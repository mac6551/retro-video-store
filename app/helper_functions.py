from flask import abort, request, make_response
from .routes import *
from app import db

def valid_id(model, id, model_string):
    """Returns instance of model with matching ID.
        Returns 404 error with custom message if object not found."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})

    model = model.query.get(id)
    if not model: 
        abort(make_response({"message": f"{model_string} {id} was not found"}, 404))

    return model

def valid_input(request_body, input):
    if input not in request_body:
        abort(400, {"details": f"Request body must include {input}."})

