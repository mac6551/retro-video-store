from flask import abort, request
from .routes import *
from app import db

# GET HELP WITH THIS FRIEND
def valid_id(model, id):
    """Returns instance of model with matching ID."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})
    
    model = model.query.get(id)

    # if not model: 
    #     abort(404, {"message": f"{model} {id} was not found"})

    return model

def valid_input(request_body, input):
    if input not in request_body:
        abort(400, {"details": f"Request body must include {input}."})

def add_to_database(item):
    db.session.add(item)
    db.session.commit()

def remove_from_database(item):
    db.session.delete(item)
    db.session.commit()
