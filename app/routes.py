from flask import Blueprint, jsonify, request, abort
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import date
from dotenv import load_dotenv
import requests
import os

load_dotenv()
customer_bp = Blueprint("customer", __name__, url_prefix = "/customers")
video_bp = Blueprint("video", __name__, url_prefix = "/videos")

def valid_id(model, id):
    """If ID is an int, returns the model object with that ID.
        If ID is not an int, returns 400.
        If model object with that ID doesn't exist, returns 404."""
    try:
        id = int(id)
    except:
        abort(400, {"error": "invalid id"})
    return model.query.get(id)

@customer_bp.route("", methods = ["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]

    return jsonify(customers_response), 200

@customer_bp.route("/<id>", methods = ["GET"])
def get_one_customer(id):
    customer = valid_id(Customer, id)
    
    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    customer = customer.to_dict()

    return customer, 200