""" db model for nft marketplace """
import datetime
from turtle import back
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# db design
""" TODO: add table for NFT Token offer (status: deline, accept) """


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    # TODO: have xrp_account to be primary key - easier workflow
    # connect wallet -> xumm -> have them sign something. 
    xrp_account = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    # TODO: have them sign nounce/current time
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    profile_photo = db.Column(
        db.String(255), nullable=True, default="https://i.imgur.com/tdi3NGa.jpg")
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    xumm_user_token = db.Column(db.String(255), nullable=True)
    nfts = db.relationship('Nft', backref="owners")
    transactions = db.relationship(
        'Transaction', secondary="transactions_users", backref="users")
    auctions = db.relationship(
        "Auction", secondary="auctions_users", backref="bidders")

    def get_nfts(self):
        return self.nfts

    def to_dict(self):
        # TODO: return more things
        return {
            "id": self.id,
            "xrp_account": self.xrp_account,
            "xumm_user_token": self.xumm_user_token,
            "email": self.email,
        }


class Nft(db.Model):
    """ table for storing nft metas """
    __tablename__ = 'nfts'
    token_id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    uri = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    owner_xrp_account = db.Column(db.Integer, db.ForeignKey(
        "users.xrp_account"), nullable=False)

    @property
    def get_owner(self):
        return self.owner_xrp_account

    def to_dict(self):
        return {
            "token_id": self.token_id,
            "title": self.title,
            "description": self.description,
            "uri": self.uri,
            "owner": self.owner_xrp_account,
        }


class Auction(db.Model):
    """ table for storing NFT auctions """
    __tablename__ = "auctions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_xrp_account = db.Column(db.Integer, db.ForeignKey(
        "users.xrp_account"), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    end_at = db.Column(db.DateTime(timezone=True),
                       server_default=func.now() + datetime.timedelta(days=1),
                       nullable=False)
    # TODO: duration = db.column(db.Interval())
    # timer solution
    nft_id = db.relationship(
        db.Integer, db.ForeignKey("nfts.id"))
    starting_price = db.Column(db.Float, nullable=False)
    # hours?
    duration = db.Column(db.Integer, nullable=False)
    current_highest_price = db.Column(db.Float)
    current_highest_bidder = db.Column(
        db.Integer, db.ForeignKey("users.xrp_account"))
    highest_offer_id = db.Column(db.String, nullable=True)
    isActive = db.Column(db.Boolean, nullable=False, default=True)
    winner = db.Column(db.Integer, db.ForeignKey("users.xrp_account"))
    # don't need a joint table because it's a one-to-many relationship
    bids = db.relationship("Bid", backref="auctions")
    bidders = db.relationship(
        "AuctionUser", secondary='auctions_users', backref="users")

    def to_dict(self):
        return {
            "id": self.id,
            "owner": self.owner_xrp_account,
            "created_at": self.created_at,
            "nft_id": self.nft_id,
            "starting_price": self.starting_price,
            "duration": self.duration,
            "current_highest_price": self.current_highest_price,
            "current_highest_bidder": self.current_highest_bidder,
            "winner": self.winner,
            "bids": self.bids,
            "bidders": self.bidders,
        }

    # minimum increment
    # TODO: add relationship backrefs for bidders
    # bidders = db.relationship()
    # store all the info about all the bids - history of all the previous bids
    def check_expiration():
        return None

    # function to check for expiration, if it's within last 10 mins, a bid is made, then extend by 10 mins
    def extend_auction(self):
        return None


class AuctionUser(db.Model):
    """ joint table for auctions and bidders """
    __tablename__ = "auctions_users"
    auction_id = db.Column(db.Integer,
                           db.ForeignKey("auctions.id"),
                           primary_key=True)
    user_xrp_acount = db.Column(db.Integer,
                                db.ForeignKey("users.xrp_acount"),
                                primary_key=True)
    last_bid_price = db.Column(db.Float)


class Bid(db.Model):
    """ table for individual bids """
    __tablename__ = "bids"
    ledger_idx = db.Column(db.String, primary_key=True)
    auction_id = db.Column(db.Integer,
                           db.ForeignKey("auctions.id"))
    xrp_account = db.Column(db.Integer,
                            db.ForeignKey("users.xrp_account"),
                            primary_key=True)
    bid_time = db.Column(db.DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False)
    bid_amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "ledger_idx": self.ledger_idx,
            "auction_id": self.auction_id,
            "xrp_account": self.xrp_account,
            "bid_time": self.bid_time,
            "bid_amount": self.bid_amount,
        }


class Transaction(db.Model):
    """ Table for nft transactions"""
    __tablename__ = "transactions"
    # id represented by ledger entry
    id = db.Column(db.Integer, primary_key=True)
    nft_id = db.Column(db.Integer, db.ForeignKey("nfts.id"))
    buyer = db.Column(db.Integer, db.ForeignKey("users.xrp_account"))
    seller = db.Column(db.Integer, db.ForeignKey("users.xrp_account"))
    price = db.Column(db.Float, nullable=False, default=0)
    transaction_time = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey(
        "auctions.id"), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nft_id": self.nft_id,
            "buyer": self.buyer,
            "seller": self.seller,
            "price": self.price,
            "transaction_time": self.transaction_time,
            "auction_id": self.auction_id,
        }


class TransactionUser(db.Model):
    """ Joint Table for nft transactions and users"""
    __tablename__ = "transactions_users"
    transaction_id = db.Column(db.Integer,
                               db.ForeignKey("transactions.id"),
                               primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.xrp_account"),
                        primary_key=True)
