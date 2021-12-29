""" db model for nft marketplace """
import datetime
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import IntRangeType

db = SQLAlchemy()

# db design
""" TODO: add table for NFT Token offer (status: deline, accept) """


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, , autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    profile_photo = db.Column(
        db.String(255), nullable=False, default="https://i.imgur.com/tdi3NGa.jpg")
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    nfts = db.relationship('Nft', backref="user")
    transactions = db.relationship('TransactionUser', backref="user")
    auctions = db.relationship("AuctionUser", backref="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_nfts(self):
        return self.nfts

    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }


class Nft(db.Model):
    """ table for storing nft metas """
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

    @property
    def get_owner(self):
        return self.owner_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "uri": self.uri,
            "owner": self.owner_id,
        }


class Auction(db.Model):
    """ table for storing NFT auctions """
    __tablename__ = "auctions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    end_at = db.Column(db.DateTime(timezone=True),
                       server_default=func.now() + datetime.timedelta(days=1),
                       nullable=False)
    # TODO: duration = db.column(db.Interval())
    # timer solution
    nft_id = db.relationship(
        db.Integer, db.ForeignKey("nfts.id"), nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    # need to be tested
    duration = db.Column(IntRangeType)
    current_highest_price = db.Column(db.Float)
    current_highest_bidder = db.Column(
        db.Integer, db.ForeignKeyf("users.id"))
    winner = db.Colunmn(db.Integer, db.ForeignKey("users.id"))
    bids = db.relationship("Bid")

    # minimum increment
    # TODO: add relationship backrefs for bidders
    # bidders = db.relationship()
    # store all the info about all the bids - history of all the previous bids
    def check_expiration():
        return None

    # function to check for expiration, if it's within last 10 mins, a bid is made, then extend by 10 mins
    def extend_auction(self):
        return None


class AuctionUser(db.model):
    """ joint table for auctions and bidders """
    __tablename__ = "auctions_users"
    auction_id = db.Column(db.Integer,
                           db.ForeignKey("auctions.id"),
                           primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)
    last_bid_price = db.Column(db.Float)
    user = db.relationship('User', backref="actions_users")


class Bid(db.model):
    """ table for individual bids """
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    auction_id = db.Column(db.Integer,
                           db.ForeignKey("auctions.id"))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)
    bid_time = db.Column(db.DateTime(timezone=True),
                         server_default=func.now(),
                         nullable=False)
    bid_amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "auction_id": self.auction_id,
            "user_id": self.user_id,
            "bid_time": self.bid_time,
            "bid_amount": self.bid_amount,
        }


class Transaction(db.model):
    """ Table for nft transactions"""
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nft_id = db.Column(db.Integer, db.ForeignKey("nfts.id"))
    buyer = db.Column(db.Integer, db.ForeignKey("users.id"))
    seller = db.Column(db.Integer, db.ForeignKey("users.id"))
    price = db.Column(db.float, nullable=False, default=0)
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


class TransactionUser(db.model):
    """ Joint Table for nft transactions and users"""
    __tablename__ = "transactions_users"
    transaction_id = db.Column(db.Integer,
                               db.ForeignKey("transactions.id"),
                               primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        primary_key=True)
