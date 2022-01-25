from flask import Blueprint, request
from flask_login import login_required, current_user
from app.models import User, Nft, Transaction, Auction,  db
from app.nft_transactions.xumm import store_user_token, get_xrp_account
webhook_routes = Blueprint('webhook', __name__)


@webhook_routes.route("/", methods=["POST"])
def receive_webhook():
    data = request.json
    user_token = ""
    if data["custom_meta"]["instruction"] == "user_sign_in_token":
        # store user token
        user_token = data['meta']['userToken']["user_token"]
        user_id = data['meta']["custom_meta"]["identifier"]
        payload_id = data['meta']['payload_uuidv4']
        xrp_account_address = get_xrp_account(payload_id)
        # TODO: auto update token after certain amount of time
        store_user_token(user_id, user_token, xrp_account_address)
        return {'msg': "user token and account address successfully stored"}
    return


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
