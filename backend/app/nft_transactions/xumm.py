import requests
import os
from dotenv import load_dotenv
import json
from models import User, db


load_dotenv()
url = "https://xumm.app/api/v1/platform/payload"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": os.getenv("XUMM_APP_KEY"),
    "X-API-Secret": os.getenv("XUMM_APP_SECRET"),
}


def get_transaction_id(payload_id):
    response = requests.request(
        "GET", url + "/" + payload_id, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    return data["response"]["txid"]

# response = requests.request(
#         "GET", url + "/" + "4691575d-5c52-4a6f-8278-c6b3f15c47e9", headers=headers)
# data = json.loads(response.content.decode('utf-8'))
# print(data)


def sign_transactions(transaction_dict, user_token, custom_meta):
    # TODO: take in meta data
    """ given the trasaction payload and the user_token, send xumm user a push notificaiton to sign the payload"""
    payload = {"txjson": transaction_dict,
               "user_token": user_token, "custom_meta": custom_meta}
    # TODO: convert the format for TransactionType and TokenTaxon later
    # print(payload)
    # if the user doesn't have push, add route to send transaction sign qr code
    response = requests.request("POST", url, json=payload, headers=headers)
    # convert byte string to dict
    data = json.loads(response.content.decode('utf-8'))
    print(data, "here")
    if not data["pushed"]:
        return {"png_url":  response.content["refs"]["qr_png"]}
    else:
        return {"pushed": True}


def user_sign_in():
    """ generate a QR code for user to scan, should get user_token in return for storage """
    payload = {
        "txjson": {
            "TransactionType": "SignIn",
            "expire": 240,
        },
        "custom_meta": {"instruction": "user_sign_in_token"}
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    print(data)
    png_url = data["refs"]["qr_png"]
    return {"png_url": png_url}


def get_xrp_account(payload_id):
    response = requests.request(
        "GET", url + "/" + payload_id, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    # TODO: store as cookie on the browser, representing them as login
    print(data["response"]["account"])
    return data["response"]["account"]

# response = requests.request(
#     "GET", url + "/" + "abf91ee3-b4b8-4404-94ac-ee72d27687bf", headers=headers)
# data = json.loads(response.content.decode('utf-8'))
# print(data["response"])


# response = requests.request(
#     "GET", url + "/" + "feb49af9-72bf-434c-8607-852633cd0d9f", headers=headers)
# data = json.loads(response.content.decode('utf-8'))
# # This is to get Payload
# response = requests.request(
#       "GET", url + "/" + "0e3f7226-4269-4b9d-a288-04973ab6083d", headers=headers)
# data = json.loads(response.content.decode('utf-8'))
# print(data)

""" {'meta': {'exists': True, 'uuid': '6e314cfb-3d31-4031-985b-ac6984a8cca4', 'multisign': False, 'submit': True, 'destination': '', 'resolved_destination': '', 'resolved': True, 'signed': True, 'cancelled': False, 'expired': False, 'pushed': True, 'app_opened': True, 'opened_by_deeplink': True, 'return_url_app': None, 'return_url_web': None, 'is_xapp': False}, 'application': {'name': 'xumm wallet nft markeplace intergration', 'description': 'xumm wallet integration for nft marketplace on xrpl', 'disabled': 0, 'uuidv4': '8c9c69e2-9e90-4ce5-92d5-1b379ff95777', 'icon_url': 'https://xumm-cdn.imgix.net/app-logo/f7e00f31-a3f7-40f0-91f5-7ff1b7bb2b5b.jpeg', 'issued_user_token': 'e5899868-642f-4680-9718-ba563af0c8ab'}, 'payload': {'tx_type': 'NFTokenMint', 'tx_destination': '', 'tx_destination_tag': None, 'request_json': {'account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8', 'TransactionType': 'NFTokenMint', 'fee': '10', 'sequence': 666082, 'flags': 0, 'last_ledger_sequence': 716371, 'signing_pub_key': '', 'TokenTaxon': 0, 'uri': '68747470733a2f2f697066732e696f2f697066732f6261666b72656967617036787a6a33337a34663732736c377163336262636b7371336b3236626a74657662746669763376706666637877637a6734'}, 'origintype': 'PUSH_NOTIFICATION', 'signmethod': 'BIOMETRIC', 'created_at': '2022-02-08T17:27:33Z', 'expires_at': '2022-02-09T17:27:33Z', 'expires_in_seconds': 86278}, 'response': {'hex': '120019228000000024000A29E3201B000AEF79202A0000000068400000000000000F732103DD699122D87D789ADAD5FF0521572BA28B3BAFBD77FE35F70CEB74D04DEE8B2B7447304502210083DCE6C8BE24C521A8847F46A61F9B2EEFAE002445FCF6A5A971B163D2CFEBFD0220415DBB00E545D8D2F252A413C41D39E874B2AF7D2D688893CD00F56BC761CB548114F7F917332EB18C40B065F37B729B4FB750A010D4', 'txid': 'D5A41F0E9D530E37CF1042651A7F24B595AED79E61844A0AE04BD6C26F6A61EF', 'resolved_at': '2022-02-08T17:27:44.000Z', 'dispatched_to': '', 'dispatched_result': 'tesSUCCESS', 'dispatched_nodetype': 'CUSTOM', 'multisign_account': '', 'account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8'}, 'custom_meta': {'identifier': None, 'blob': None, 'instruction': None}}
rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8 """


def store_user_token(user_token, account_address):
    """ utitlity function to store user token in database, get called by webhook route when signin payload received"""
    # TODO: maybe have a seperate function for new sign up and sign in.
    
    user = User.query.get(account_address)
    if not user:
        user = User(xrp_account=account_address, xumm_user_token=user_token)
        db.session.add(User)
    # TODO: store the expiration. 12 months expiration date.
    else:
        user.xumm_user_token = user_token
    db.session.commit()
