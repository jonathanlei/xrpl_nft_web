""" This is a utility script for running the open-bid english auction
detailed rules: 
1. Seller set starting price, if not set the minimum amount will be 1 XRP 
2. Seller set duration (1 hour -7 days?), default duration is 1 day (24 hours)
3. Auctions can be extended within the last 10 minutes of bidding window, if a new bid has been submitted, by 10 minutes. 
4. Seller have the option to cancel the auction anytime before the end of the auction window
5. Seller can set a buy now button? (optinoal, more complexities)
"""

from models import db, Auction, User, Bid


def open_auction(owner, token_id, starting_price, duration=1):
    auction = Auction(owner=owner, duration=duration,
                      starting_price=starting_price, nft_id=token_id)
    db.session.add(auction)
    db.session.commit()
    return auction.to_dict()


def new_bid(bidder, auction_id, price):
    return None
