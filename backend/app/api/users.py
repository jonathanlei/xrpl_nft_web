from flask import Blueprint, jsonify, session, request
from models import User, Nft, Transaction, Auction,  db
from aws import (
    upload_file_to_s3, allowed_file, get_unique_filename)
from nft_transactions.xumm import user_sign_in
from flask_cors import CORS, cross_origin
user_routes = Blueprint('users', __name__)

""" TODO: add wallet intergration and add wallet route """

CORS(user_routes)


@user_routes.route('/')
def get_all_users():
    users = User.query.all()
    return {"users": [user.to_dict() for user in users]}


@user_routes.route("/connect-wallet")
def connect_wallet():
    png_url = user_sign_in()
    return png_url


@user_routes.route('/<string:xrp_account>')
def get_user(xrp_account):
    user = User.query.get(xrp_account)
    return user.to_dict()


@user_routes.route("/update/", methods=["PUT"])
def update_user():
    print("inside update user")
    data = request.json
    user = User.query.filter(User.id == current_user.id).one()
    user.email = data["email"]
    db.session.commit()
    return user.to_dict()


@user_routes.route("/update/image/", methods=["PATCH"])
def update_profile_photo():
    """ TODO: Domain is cool to use; there is also EmailHash, 
    which is sometimes used to look up 
    avatars from Gravatar 
    (which maps email hashes to profile pictures) """
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


@user_routes.route("/<string:xrp_account>/transactions")
def get_all_transactions(xrp_account):
    all_transactions = Transaction.query.filter(
        Transaction.buyer == xrp_account, Transaction.seller == xrp_account).all()
    return {"transactions": [n.to_dict() for n in all_transactions]}


@user_routes.route("/<string:xrp_account>/nfts")
def get_all_nfts(xrp_account):
    all_nfts = Nft.query.filter(Nft.owner_xrp_account == xrp_account).all()
    return {"nfts": [n.to_dict() for n in all_nfts]}


@user_routes.route("/<string:xrp_account>/auctions")
def get_all_auctions(xrp_account):
    all_nfts = Nft.query.filter(Nft.owner_xrp_account == xrp_account).all()
    return {"nfts": [n.to_dict() for n in all_nfts]}


@user_routes.route("/", methods=["DELETE"])
def delete_user():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    return {"msg": "User deleted successfully"}, 200
# TODO: get bids?
