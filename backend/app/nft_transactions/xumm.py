import requests
import os
from dotenv import load_dotenv
from app.models import User, db


load_dotenv()
url = "https://xumm.app/api/v1/platform/payload"
print(os.getenv("XUMM_APP_SECRET"))


def sign_transactions(transaction_dict, user_token):
    """ given the trasaction payload and the user_token, send xumm user a push notificaiton to sign the payload"""
    payload = {"txjson": transaction_dict, user_token: "user_token"}

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("XUMM_APP_KEY"),
        "X-API-Secret": os.getenv("XUMM_APP_SECRET"),
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.content)
    return response


trasaction_dict = {
    "txjson": {
        "TransactionType": "Payment",
        "Destination": "rPdvC6ccq8hCdPKSPJkPmyZ4Mi1oG2FFkT",
        "Fee": "12"
    },
    "user_token": 'e5899868-642f-4680-9718-ba563af0c8ab',
}

sign_transactions(trasaction_dict)


def user_sign_in(id):
    """ generate a QR code for user to scan, should get user_token in return for storage """
    payload = {
        "txjson": {
            "TransactionType": "SignIn",
            "expire": 240,
            "custom_meta": {"identifier": id, "instruction": "user_sign_in_token"}
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-Key": os.getenv("XUMM_APP_KEY"),
        "X-API-Secret": os.getenv("XUMM_APP_SECRET"),
    }
    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.content)
    data = response.content
    png_url = data["refs"]["qr_png"]
    # TODO: send the png to frontend


def store_user_token(id, user_token):
    """ utitlity function to store user token in database"""
    user = User.query.get(id)
    user.xumm_user_token = user_token
    db.session.commit()


""" 
"uuid":"a98fab1f-9553-4c96-88c9-f7439de5e8dd",
"next":{"always":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd"},
"refs":{"qr_png":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd_q.png",
"qr_matrix":"https://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd_q.json",
"qr_uri_quality_opts":["m","q","h"],
"websocket_status":"wss://xumm.app/sign/a98fab1f-9553-4c96-88c9-f7439de5e8dd"},"pushed":false}'
 """


""" 
 user token 
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
