from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from models import User, Nft, Transaction, Auction,  db
from aws import (
    upload_file_to_s3, allowed_file, get_unique_filename)
from datetime import datetime
from auction_utils import new_bid
from nft_transactions.transact import createNftBuyOffer
auction_routes = Blueprint('auctions', __name__)


@auction_routes.route('/')
def get_all_actions():
    auctions = Auction.query.all()
    return {"auctions": [auction.to_dict() for auction in auctions]}


@auction_routes.route('/<int:id>')
def get_auction(id):
    auction = Auction.query.get(id)
    return auction.to_dict()


@auction_routes.route("/new", methods=["PUT"])
@login_required
def create_new_action():
    data = request.json
    auction = Auction(owner=current_user.id, nft_id=data["nft_id"],
                      starting_price=data["starting_price"],
                      duration=data["duration"])
    db.session.add(auction)
    db.session.commit()
    return auction.to_dict()


@auction_routes.route("/<int:id>/new_bid", methods=["PUT"])
@login_required
def create_new_bid(id):
    # TODO: frontend filter out lower prices so price check here
    data = request.json
    auction = Auction.query.get(id)
    new_offer = createNftBuyOffer(
        auction.id, auction.owner, current_user.id, auction.nft_id, data["price"])
    return new_offer


@auction_routes.route("/<int:id>/extend", methods=["PATCH"])
@login_required
def extend_auction(id):
    data = request.json
    auction = Auction.query.get(id)
    # TODO: determine end up format from frontend and convert
    # to datetime object using "datetime.strptime"
    if data["end_at"] > auction.end_at:
        auction.end_at = data["end_at"]
        db.session.commit()
    else:
        return {"msg": "User can only extend, not shorten the auction"}, 400
    return auction.to_dict()


@auction_routes.route("/<int:id>/cancel", methods=["DELETE"])
@login_required
def delete_auction(id):
    auction = Auction.query.get(id)
    if datetime.now() > auction.end_at:
        return {"msg": "cannot cancel auction that's already closed"}, 400
    db.session.delete(auction)
    db.session.commit()
    return {"msg": "Auction canceled successfully"}, 200
