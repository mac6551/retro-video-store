from flask import Blueprint, jsonify, request, abort
from flask.wrappers import Request
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import date, datetime
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

@customer_bp.route("", methods = ["POST"])
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body:
        return {"details": "Request body must include name."}, 400
    if "phone" not in request_body:
        return {"details": "Request body must include phone."}, 400
    if "postal_code" not in request_body:
        return {"details": "Request body must include postal_code."}, 400
    
    new_customer = Customer(name = request_body["name"],
                            phone = request_body["phone"],
                            postal_code = request_body["postal_code"])

    db.session.add(new_customer)
    db.session.commit()
    return {"id": new_customer.id}, 201

@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_one_customer(id):
    customer = valid_id(Customer, id)

    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()
    return {"id": int(id)}, 200

@customer_bp.route("/<id>", methods = ["PUT"])
def update_one_customer(id):
    customer = valid_id(Customer, id)

    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    request_body = request.get_json()

    if "name" not in request_body or "phone" not in request_body \
        or "postal_code" not in request_body:
        return {"details": "invalid data"}, 400

    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]

    customer = customer.to_dict()
    db.session.commit()

    return customer, 200

@video_bp.route("", methods = ["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = [video.to_dict() for video in videos]

    return jsonify(videos_response), 200


@video_bp.route("/<id>", methods = ["GET"])
def get_one_video(id):
    video = valid_id(Video, id)
    
    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    video = video.to_dict()

    return video, 200

@video_bp.route("", methods = ["POST"])
def create_video():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Request body must include title."}, 400
    if "release_date" not in request_body:
        return {"details": "Request body must include release_date."}, 400
    if "total_inventory" not in request_body:
        return {"details": "Request body must include total_inventory."}, 400
    
    new_video = Video(title = request_body["title"],
                            release_date = request_body["release_date"],
                            total_inventory = request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()
    return {"id": new_video.id}, 201

