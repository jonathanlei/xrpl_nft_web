import requests
import os
from dotenv import load_dotenv
from models import User, db


load_dotenv()
url = "https://xumm.app/api/v1/platform/payload"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": os.getenv("XUMM_APP_KEY"),
    "X-API-Secret": os.getenv("XUMM_APP_SECRET"),
}
response = requests.request(
    "GET", url + "/74ba68e4-6714-47dd-9af1-fbe252a9769c", headers=headers)


def sign_transactions(transaction_dict, user_token):
    """ given the trasaction payload and the user_token, send xumm user a push notificaiton to sign the payload"""
    payload = {"txjson": transaction_dict, user_token: "user_token"}
    # if the user doesn't have push, add route to send transaction sign qr code
    response = requests.request("POST", url, json=payload, headers=headers)
    if not response.content["pushed"]:
        return {"png_url":  response.content["refs"]["qr_png"]}
    else:
        return {"pushed": True}


def user_sign_in(id):
    """ generate a QR code for user to scan, should get user_token in return for storage """
    payload = {
        "txjson": {
            "TransactionType": "SignIn",
            "expire": 240,
            "custom_meta": {"identifier": id, "instruction": "user_sign_in_token"}
        }
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.content
    png_url = data["refs"]["qr_png"]
    return {"png_url": png_url}


def get_xrp_account(payload_id):
    response = requests.request(
        "GET", url + "/" + payload_id, headers=headers)
    data = response.content
    return data["response"]["account"]


def store_user_token(id, user_token, account_address):
    """ utitlity function to store user token in database, get called by webhook route when signin payload received"""
    user = User.query.get(id)
    user.xumm_user_token = user_token
    user.xrp_account_id = account_address
    db.session.commit()


""" 
response.content
"uuid":"a98fab1f-9553-4c96-88c9-f7439de5e8dd",
"next":{"always":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd"},
"refs":{"qr_png":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd_q.png",
"qr_matrix":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd_q.json",
"qr_uri_quality_opts":["m","q","h"],
"websocket_status":"wss://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd"},
"pushed":false}'
 """


""" 
 user token from payload webhook
 {
  "meta": {
    "url": "https://webhook.site/ee978f52-ae51-4c2e-bba7-c053ed972c7d",
    "application_uuidv4": "8c9c69e2-9e90-4ce5-92d5-1b379ff95777",
    "payload_uuidv4": "74ba68e4-6714-47dd-9af1-fbe252a9769c",
    "opened_by_deeplink": true
  },
  "custom_meta": {
    "identifier": null,
    "blob": null,
    "instruction": null
  },
  "payloadResponse": {
    "payload_uuidv4": "74ba68e4-6714-47dd-9af1-fbe252a9769c",
    "reference_call_uuidv4": "9a793c76-22c6-4ed2-b44b-04a44f17f92e",
    "signed": true,
    "user_token": true,
    "return_url": {
      "app": null,
      "web": null
    }
  },
  "userToken": {
    "user_token": "e5899868-642f-4680-9718-ba563af0c8ab",
    "token_issued": 1642547929,
    "token_expiration": 1645139929
  }
}
"""
""" 
{

    "meta": {
        "exists": true,
        "uuid": "74ba68e4-6714-47dd-9af1-fbe252a9769c",
        "multisign": false,
        "submit": false,
        "destination": "",
        "resolved_destination": "",
        "resolved": true,
        "signed": true,
        "cancelled": false,
        "expired": true,
        "pushed": false,
        "app_opened": true,
        "opened_by_deeplink": true,
        "return_url_app": null,
        "return_url_web": null,
        "is_xapp": false,
    },
    "application": {
        "name": "xumm wallet nft markeplace intergration",
        "description": "xumm wallet integration for nft marketplace on xrpl",
        "disabled": 0,
        "uuidv4": "8c9c69e2-9e90-4ce5-92d5-1b379ff95777",
        "icon_url": "https://xumm-cdn.imgix.net/app-logo/f7e00f31-a3f7-40f0-91f5-7ff1b7bb2b5b.jpeg",
        "issued_user_token": null,
    },
    "payload": {
        "tx_type": "SignIn",
        "tx_destination": "",
        "tx_destination_tag": null,
        "request_json": {"TransactionType": "SignIn", "SignIn": true},
        "origintype": "DEEP_LINK",
        "signmethod": "BIOMETRIC",
        "created_at": "2022-01-18T23:18:05Z",
        "expires_at": "2022-01-19T23:18:05Z",
        "expires_in_seconds": -519503,
    },
    "response": {
        "hex": "732103DD699122D87D789ADAD5FF0521572BA28B3BAFBD77FE35F70CEB74D04DEE8B2B74473045022100DDFC3CC1750859F4F71CFF803C01D9E6649926C0624CD6348AC5309E39DE1AB5022070CDBD4229877EA4D8A342F2F2860FABC7A0ED030ACD05CEE27D80F613D12D478114F7F917332EB18C40B065F37B729B4FB750A010D4",
        "txid": "FA70917E8F726B1F002AFFC01C31D6141A025E1ED8E978DD561EAD9F0BB0EE02",
        "resolved_at": "2022-01-18T23:18:49.000Z",
        "dispatched_to": "",
        "dispatched_result": "",
        "dispatched_nodetype": "",
        "multisign_account": "",
        "account": "rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8",
    },
    "custom_meta": {"identifier": null, "blob": null, "instruction": null},
} """
