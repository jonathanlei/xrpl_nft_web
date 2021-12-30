from flask import Blueprint, jsonify, session, request
from flask_login import login_required, current_user
from app.models import User, Nft, Transaction, Auction,  db

from sqlalchemy.sql import func

auction_routes = Blueprint('auctions', __name__)

""" TODO: add wallet intergration and add wallet route """


@auction_routes.route('/')
def auctions():
    auctions = Auction.query.all()
    return {"auctions": [auctions.to_dict() for nft in auctions]}


@auction_routes.route("/active")
def active_auctions():
    active_auctions = Auction.query.filter(Auction.end_at >= func.now())


@auction_routes.route('/<int:id>')
def nft(id):
    nft = Nft.query.get(id)
    return nft.to_dict()


""" class Nft(db.Model):
     table for storing nft metas 
    __tablename__ = 'nfts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    uri = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)
 """

# TODO: Should we show previous transactions? Auction history?


@auction_routes.route("/<int:id>/transactions")
def get_all_transactions(id):
    all_transactions = Transaction.query.filter(
        Transaction.buyer == id, Transaction.seller == id).all()
    return {"transactions": [n.to_dict() for n in all_transactions]}


@auction_routes.route("/<int:id>/nfts")
def get_all_nfts(id):
    all_nfts = Nft.query.filter(Nft.owner_id == id).all()
    return {"nfts": [n.to_dict() for n in all_nfts]}

# TODO: check how to do this
# @auction_routes.route("/<int:id>/auctions")
# def get_all_auctions(id):
#     all_auctions = Auction.query.filter(Auction.owner_id == id).all()
#     return {"auctions": [n.to_dict() for n in all_auctions]}


@auction_routes.route("/", methods=["DELETE"])
@login_required
def delete_user():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    return {"msg": "User deleted successfully"}, 200
