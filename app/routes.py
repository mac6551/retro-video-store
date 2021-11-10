from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.video import Video
from app.models.video import Rental
from datetime import date, timedelta
from .helper_functions import *
from app import db
from dotenv import load_dotenv

load_dotenv()

customer_bp = Blueprint("customer", __name__, url_prefix = "/customers")
video_bp = Blueprint("video", __name__, url_prefix = "/videos")
rental_bp = Blueprint("rental", __name__, url_prefix = "/rentals")

@customer_bp.route("", methods = ["GET"])
def get_customers():
    """Returns list of dictionaries of customer info."""
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]

    return jsonify(customers_response), 200

@customer_bp.route("/<id>", methods = ["GET"])
def get_one_customer(id):
    """Returns dictionary of customer info with matching ID."""
    customer = valid_id(Customer, id)
    
    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    customer = customer.to_dict()

    return customer, 200

@customer_bp.route("", methods = ["POST"])
def create_customer():
    """Adds customer to database and returns new customer ID and 201."""
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
    """Deletes customer and returns ID of deleted customer."""
    customer = valid_id(Customer, id)

    if not customer: 
        return {"message": f"Customer {id} was not found"}, 404

    db.session.delete(customer)
    db.session.commit()
    return {"id": int(id)}, 200

@customer_bp.route("/<id>", methods = ["PUT"])
def update_one_customer(id):
    """Updates cusomter in database and \
        returns dictionary with updated customer infomation."""
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
    """Returns list of dictionaries of video info"""
    videos = Video.query.all()
    videos_response = [video.to_dict() for video in videos]

    return jsonify(videos_response), 200


@video_bp.route("/<id>", methods = ["GET"])
def get_one_video(id):
    """Returns dictionary of video info with matching ID."""
    video = valid_id(Video, id)
    
    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    video = video.to_dict()

    return video, 200

@video_bp.route("", methods = ["POST"])
def create_video():
    """Creates video in database and returns new video ID and 201 if successful."""
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

    return new_video.to_dict(), 201

@video_bp.route("/<id>", methods = ["DELETE"])
def delete_one_video(id):
    """Deletes video from database and returns ID of deleted video."""
    video = valid_id(Video, id)

    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    db.session.delete(video)
    db.session.commit()
    return {"id": int(id)}, 200

@video_bp.route("/<id>", methods = ["PUT"])
def update_one_video(id):
    """Updates video in database and \
    returns dictionary with updated video infomation."""
    video = valid_id(Video, id)

    if not video: 
        return {"message": f"Video {id} was not found"}, 404

    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body \
        or "total_inventory" not in request_body:
        return {"details": "invalid data"}, 400

    video.title = request_body["title"]
    video.total_inventory = request_body["total_inventory"]
    video.release_date = request_body["release_date"]

    video = video.to_dict()
    db.session.commit()

    return video, 200

def create_checked_out_inventory():
    checked_out_inventory = {}
    videos = Video.query.all()
    for video in videos:
        checked_out_inventory[video.id] = 0
    return checked_out_inventory

def calculate_available_inventory(video):
    checked_out_inventory = create_checked_out_inventory()

    if video not in checked_out_inventory:
        checked_out_inventory[video] = 0
    checked_out_inventory[video] += 1
    available_inventory = video.total_inventory - checked_out_inventory[video.id]
    return available_inventory

@rental_bp.route("check-out", methods = ["POST"])
def check_video_in_or_out(): 
    request_body = request.get_json()

    if "customer_id" not in request_body:
        return {"details": "Request body must include customer_id."}, 400
    if "video_id" not in request_body:
        return {"details": "Request body must include video_id."}, 400

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    due_date = date.today() + timedelta(7) 
    customer = valid_id(Customer, customer_id)
    video = valid_id(Video, video_id)
    
    if not customer: 
        return {"message": f"Customer {customer_id} was not found"}, 404
    if not video: 
        return {"message": f"Video {video_id} was not found"}, 404

    new_rental = Rental(due_date = due_date,
                        customer_id = customer_id,
                        video_id = video_id)

    db.session.add(new_rental)
    db.session.commit()

    available_inventory = calculate_available_inventory(new_rental.video)
    videos_checked_out_count = 0
    videos_checked_out_count += 1

    if available_inventory < 0:
        return {"message": "Could not perform checkout"}, 400

    return {
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": videos_checked_out_count,
            "available_inventory": available_inventory
        }