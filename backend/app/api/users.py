from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from app.models import User, Nft
from app.aws import (
    upload_file_to_s3, allowed_file, get_unique_filename)

user_routes = Blueprint('users', __name__)

""" TODO: add wallet intergration and add wallet route """
@user_routes.route('/')
@login_required
def users():
    users = User.query.all()
    return {"users": [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    user = User.query.get(id)
    return user.to_dict()


@user_routes.route("/update/", methods=["PUT"])
@login_required
def update_user():
    print("inside update user")
    data = request.json
    user = User.query.filter(User.id == current_user.id).one()
    user.first_name = data["firstName"]
    user.last_name = data["lastName"]
    user.email = data["email"]
    db.session.commit()
    return user.to_dict()


@user_routes.route("/update/image/", methods=["PATCH"])
@login_required
def update_profile_photo():
    if "image" not in request.files:
        return {"errors": "image required"}, 400

    image = request.files["image"]

    if not allowed_file(image.filename):
        return {"errors": "file type not permitted"}, 400

    image.filename = get_unique_filename(image.filename)

    upload = upload_file_to_s3(image)

    if "url" not in upload:
        # if the dictionary doesn't have a url key
        # it means that there was an error when we tried to upload
        # so we send back that error message
        return upload, 400

    url = upload["url"]
    # flask_login allows us to get the current user from the request
    currUser = User.query.get(current_user.id)
    currUser.profile_photo = url
    db.session.commit()
    return currUser.to_dict()


@user_routes.route("/<int:id>/nfts")
def get_all_nfts(id):
    all_nfts = Nft.query.filter(Nft.owner_id == id).all()
    return {"nfts": [n.to_dict() for n in all_nfts]}


@user_routes.route("/", methods=["DELETE"])
@login_required
def delete_user():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    return {"msg": "User deleted successfully"}, 200
