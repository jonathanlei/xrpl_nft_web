""" This is a utility script for running the open-bid english auction
detailed rules: 
1. Seller set starting price, if not set the minimum amount will be 1 XRP 
2. Seller set duration (1 hour -7 days?), default duration is 1 day (24 hours)
3. Auctions can be extended within the last 10 minutes of bidding window, if a new bid has been submitted, by 10 minutes. 
4. Seller have the option to cancel the auction anytime before the end of the auction window?
5. Seller can set a buy now button? (optinoal, more complexities)
"""

from models import db, Auction, User, Bid, AuctionUser
from datetime import datetime, timedelta



def new_bid(user_id, auction_id, price):
    """ TODO: maybe it's betteer to store current_high_bid_id instead??? and reference it """
    # TODO: if the bid is smaller than current bid, disgard (could do it in the frontend too)
    bid = Bid(auction_id=auction_id, user_id=user_id, price=price)
    current_auction = Auction.query.filter(Auction.id == auction_id).one()
    # add to the relationship
    # will there be duplicates?
    bidder = User.query.get(user_id)
    current_auction.append(bidder)
    # check time, if the time is within the last 10 mins, extend the auction
    if datetime.now() + timedelta(minutes=10) > current_auction.end_at:
        current_auction.end_at = current_auction.end_at + timedelta(minutes=10)
    if price > current_auction.current_highest_price:
        current_auction.current_highest_price = price
        current_auction.current_highest_bidder = user_id
        db.session.add(bid)
        db.session.commit()
    return bid.to_dict()


def end_auction():
    # timer, display winner
    # set timeout python solution
    # detach callback, (resest timer and delete )
    """
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
    """
