""" db model for nft marketplace """
import datetime
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


""" user template from previous apps, params are adjustable """


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, , autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(), nullable=False)
    nfts = db.relationship('Nft', backref="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

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
    uri = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), nullable=False)


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
    ## TODO: duration = db.column(db.Interval())
    ## timer solution
    nft_id = db.relationship(
        db.Integer, db.ForeignKey("nfts.id"), nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    current_highest_price = db.Column(db.Float)
    current_highest_bidder = db.relationship(
        db.Integer, db.ForeignKey("users.id"))
    winner = db.relationship(db.Integer, db.ForeignKey("users.id"))
    ##minimum increment 
    # TODO: add relationship backrefs for bidders
    # bidders = db.relationship()
    # store all the info about all the bids - history of all the previous bids 


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


class Transaction(db.model):
    """ joint table for auctions and bidders """
    