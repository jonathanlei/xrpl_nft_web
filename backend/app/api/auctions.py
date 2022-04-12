from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from models import User, Nft, Transaction, Auction,  db
from aws import (
    upload_file_to_s3, allowed_file, get_unique_filename)
from datetime import datetime
from nft_transactions.xrp_transact import createNftBuyOffer
from auction_utils import end_auction_and_create_sell_offer
from worker import conn
from rq import Queue
from rq.job import Job
auction_routes = Blueprint('auctions', __name__)
# import and initialize the queue
q = Queue(connection=conn)


@auction_routes.route('/')
def get_all_actions():
    auctions = Auction.query.all()
    return {"auctions": [auction.to_dict() for auction in auctions]}


@auction_routes.route('/<int:id>')
def get_auction(id):
    auction = Auction.query.get(id)
    return {"auction": auction.to_dict()}


@auction_routes.route("/new", methods=["PUT"])
@login_required
def create_new_action():
    # TODO: determine duration data format
    # dt_string = "12/11/2018 09:15:32"
    data = request.json
    auction = Auction(owner=current_user.id, nft_id=data["nft_id"],
                      starting_price=data["starting_price"],
                      end_at=data["end_at"])
    dt_obj = datetime.strptime(data["end_at"], "%d/%m/%Y %H:%M:%S")
    db.session.add(auction)
    db.session.commit()
    job = q.enqueue_in(datetime.now()-dt_obj,
                       end_auction_and_create_sell_offer(auction.id, data["end_at"]))
    return {"auction": auction.to_dict()}


@auction_routes.route("/<int:id>/new_bid", methods=["PUT"])
@login_required
def create_new_bid(id):
    data = request.json
    auction = Auction.query.get(id)
    # TODO: current_user login - and address
    new_offer = createNftBuyOffer(
        auction.id, current_user.id, data["price"], True)
    return new_offer


@auction_routes.route("/<int:id>/extend", methods=["PATCH"])
@login_required
def extend_auction(id):
    data = request.json
    auction = Auction.query.get(id)
    # TODO: determine end up format from frontend and convert
    # to datetime object using "datetime.strptime"
    # dt_string = "12/11/2018 09:15:32"
    if data["end_at"] > auction.end_at:
        auction.end_at = data["end_at"]
        db.session.commit()
        dt_obj = datetime.strptime(data["end_at"], "%d/%m/%Y %H:%M:%S")
        job = q.enqueue_in(datetime.now()-dt_obj,
                       end_auction_and_create_sell_offer(auction.id, data["end_at"]))
    else:
        return {"msg": "User can only extend, not shorten the auction"}, 400
    return {"auction": auction.to_dict()}


@auction_routes.route("/<int:id>/cancel", methods=["DELETE"])
@login_required
def delete_auction(id):
    auction = Auction.query.get(id)
    if datetime.now() > auction.end_at:
        return {"msg": "cannot cancel auction that's already closed"}, 400
    db.session.delete(auction)
    db.session.commit()
    return {"msg": "Auction canceled successfully"}, 200
