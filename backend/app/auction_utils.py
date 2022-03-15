""" This is a utility script for running the open-bid english auction
detailed rules:
1. Seller set starting price, if not set the minimum amount will be 1 XRP
2. Seller set duration (1 hour -7 days?), default duration is 1 day (24 hours)
3. Auctions can be extended within the last 10 minutes of bidding window, if a new bid has been submitted, by 10 minutes.
4. Seller have the option to cancel the auction anytime before the end of the auction window?
5. Seller can set a buy now button? (optinoal, more complexities)



new potential work flow: 
"1) buyers submit buy offers with YOU as the destination. No expiration necessary.
    allow cancel offers
    no expiration now
set the fee to 0? and have an env 
more realistic
2) when the auction is over - you send a receipt to the seller, showing the amount you are going to take as a fee, and requesting they sign a sell offer with the amount being the best buy side offer minus your fee. You are again the destination. They must sign this.
    binding? - 1. before auction seller send offer indicate the minimum amount reserve, broker might rip off
    2. agreement to pay the fee. 
3) then you can sign the NFTokenAcceptOffer transaction to complete the tx
4) finally, you can now immediately cancel all of the losing offers, since you are the destination"
"""

from models import db, Auction, User, Bid, AuctionUser
from datetime import datetime, timedelta
from nft_transactions.xrp_transact import createNftBuyOffer, createAcceptOffer, createNftSellOffer, createAcceptOfferAndSign


# create a broker account and user token as secret
# set the receiving end to the broker account
# store auction dat off chain as well?
# create sell offer with best buy offer with fee deducted and have the sell offer


def confirm_new_bid(ledger_idx, auction_id, buyer_xrp_account, price):
    # once they sign the transactions, come back and create that
    bid = Bid(ledger_idx=ledger_idx, auction_id=auction_id,
              xrp_account=buyer_xrp_account,
              price=price)
    # find owner
    current_auction = Auction.query.filter(Auction.id == auction_id).one()
    # add to the relationship
    # will there be duplicates?
    bidder = User.query.get(buyer_xrp_account)
    current_auction.bidders.append(bidder)
    # check time, if the time is within the last 10 mins, extend the auction
    # TODO: might have to convert to datetime
    if datetime.now() + timedelta(minutes=10) > current_auction.end_at:
        current_auction.end_at = current_auction.end_at + timedelta(minutes=10)
    if price > current_auction.current_highest_price:
        current_auction.current_highest_price = price
        current_auction.current_highest_bidder = buyer_xrp_account
        current_auction.highest_bid_ledger_idx = ledger_idx
        db.session.add(bid)
        db.session.commit()
    return bid.to_dict()


def end_auction_and_create_sell_offer(auction_id, seller_xrp_account):
    auction = Auction.query.get(auction_id)
    auction.isActive = False
    auction.winner = User.query.get(seller_xrp_account)
    db.session.commit()

    # timer, display winner
    # set timeout python solution
    # detach callback, (resest timer and delete)
    return createNftSellOffer(auction_id, seller_xrp_account,
                              auction.current_highest_price, True)

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


def accept_broker_offer(auction_id, sell_offer_id):
    createAcceptOfferAndSign(auction_id, sell_offer_id)
