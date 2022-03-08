from flask import Blueprint, request
from flask_login import login_required, current_user
from nft_transactions.xumm import get_transaction_id
from models import User, Nft, Transaction, Auction,  Bid, db
from nft_transactions.xumm import store_user_token, get_xrp_account, get_transaction_id
from nft_transactions.xrp_transact import createAcceptOfferAndSign, get_nft_id, get_offer_id
from auction_utils import confirm_new_bid
import json

webhook_routes = Blueprint('webhook', __name__)


@webhook_routes.route("/", methods=["POST"])
def receive_webhook():
    data = request.json
    print("THIS IS THE WEBHOOK RECEIVING PAYLOAD", data)
    instruction = data["custom_meta"]["instruction"]
    meta = data["custom_meta"]["blob"]
    payload_id = data['meta']['payload_uuidv4']
    if instruction == "user_sign_in_token":
        # store user token
        user_token = data['meta']['userToken']["user_token"]
        user_id = meta["id"]
        xrp_account_address = get_xrp_account(payload_id)
        # TODO: auto update token after certain amount of time
        store_user_token(user_id, user_token, xrp_account_address)
        return {'msg': "user token and account address successfully stored"}
    elif instruction == "mint_nft":
        token_id = get_nft_id(payload_id=data['meta']['payload_uuidv4'])
        nft = Nft(token_id=token_id, title=meta["title"], description=meta["description"],
                  owner_id=meta["owner"], uri=meta["uri"])
        db.session.add(nft)
        db.session.commit()
        return nft.to_dict()
    elif instruction == "create_buy_offer":
        buyer_offer_id = get_offer_id(payload_id)
        return confirm_new_bid(buyer_offer_id, meta["auction_id"], meta["buyer_id"],  meta["price"])
    elif instruction == "create_sell_offer":
        sell_offer_id = get_offer_id(payload_id)
        return createAcceptOfferAndSign(meta["auction_id"], sell_offer_id)
        # create accept offer for both sides, complete transaction
    elif instruction == "create_accept_offer":
        print(data['meta'])
    return "this is webhook"

# format
{'meta':
 {'url': 'http://513d-71-202-89-74.ngrok.io/webhook/',
  'application_uuidv4': '8c9c69e2-9e90-4ce5-92d5-1b379ff95777',
  'payload_uuidv4': '5474807a-d461-461c-ba94-527c64b95821', 'opened_by_deeplink': True},
 'custom_meta': {'identifier': None, 'blob': None, 'instruction': None},
 'payloadResponse': {'payload_uuidv4':
                     '5474807a-d461-461c-ba94-527c64b95821',
                     'reference_call_uuidv4': '0e907414-6f11-4277-9882-f6e21fce5402', 'signed': True,
                     'user_token': True, 'return_url': {'app': None, 'web': None}},
 'userToken': {'user_token': 'e5899868-642f-4680-9718-ba563af0c8ab',
               'token_issued': 1643069251, 'token_expiration': 1645661251}}
