from flask import abort
from .routes import *

def valid_id(model, id):
    """Returns instance of model with matching ID."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})
    return model.query.get(id)

def calculate_available_inventory(video):
    checked_out_inventory = create_checked_out_inventory()

    if video not in checked_out_inventory:
        checked_out_inventory[video] = 0
    checked_out_inventory[video] += 1

    available_inventory = video.total_inventory - checked_out_inventory[video.id]
    return available_inventory


