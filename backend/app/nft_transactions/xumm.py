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
    data = json.loads(response.content.decode('utf-8'))
    print(data)
    png_url = data["refs"]["qr_png"]
    return {"png_url": png_url}
# user_sign_in(2)


def get_xrp_account(payload_id):
    response = requests.request(
        "GET", url + "/" + payload_id, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    # TODO: store as cookie on the browser, representing them as login
    print(data["response"]["account"])
    return data["response"]["account"]

    # get transaction details

    # NFTokenPage creation


    # Modifying NFTokenPage
""" const { convertHexToString } = require('xrpl');

module.exports = (tx, meta) => {
  const affectedNode = meta.AffectedNodes.find(
    node =>
      node?.CreatedNode?.LedgerEntryType === 'NFTokenPage' ||
      node?.ModifiedNode?.LedgerEntryType === 'NFTokenPage'
  );
  const nftNode = affectedNode.CreatedNode ?? affectedNode.ModifiedNode;

  const previousTokenIds = nftNode?.PreviousFields?.NonFungibleTokens?.map(
    token => token?.NonFungibleToken?.TokenID
  );
  const previousTokenIdSet = new Set(previousTokenIds);
  const finalTokenIds = (nftNode.FinalFields ?? nftNode.NewFields)?.NonFungibleTokens?.map(
    token => token?.NonFungibleToken?.TokenID
  );
  const tokenID = finalTokenIds.find(tid => !previousTokenIdSet.has(tid));

  return {
    tokenID,
    tokenTaxon: tx.TokenTaxon,
    uri: convertHexToString(tx.URI),
  };
}; """

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
""" {'uuid': 'eb311eab-443d-4f29-8570-3afc15cbedcf',
'next': {'always': 'https://xumm.app/sign/eb311eab-443d-4f29-8570-3afc15cbedcf'},
'refs': {'qr_png': 'https://xumm.app/sign/eb311eab-443d-4f29-8570-3afc15cbedcf_q.png',
 'qr_matrix': 'https://xumm.app/sign/eb311eab-443d-4f29-8570-3afc15cbedcf_q.json',
 'qr_uri_quality_opts': ['m', 'q', 'h'], 'websocket_status': 'wss://xumm.app/sign/eb311eab-443d-4f29-8570-3afc15cbedcf'}, 'pushed': False}
{'meta': {'exists': True, 'uuid': '6989b571-eb76-4a10-9923-18454c05f21b', 'multisign': False, 'submit': True, 'destination': '',
'resolved_destination': '', 'resolved': True, 'signed': True, 'cancelled': False, 'expired': False, 'pushed': True,
'app_opened': True, 'opened_by_deeplink': True, 'return_url_app': None, 'return_url_web': None, 'is_xapp': False},
'application': {'name': 'xumm wallet nft markeplace intergration', 'description': 'xumm wallet integration for nft marketplace on xrpl',

'disabled': 0, 'uuidv4': '8c9c69e2-9e90-4ce5-92d5-1b379ff95777',
'icon_url': 'https://xumm-cdn.imgix.net/app-logo/f7e00f31-a3f7-40f0-91f5-7ff1b7bb2b5b.jpeg', '
issued_user_token': 'e3bf2a28-a7c7-421a-a1c5-4c86b806551b'}, 'payload': {'tx_type': 'NFTokenMint', 'tx_destination': '',
 'tx_destination_tag': None, 'request_json': {'account': 'rGaqbQwA2PFEQETV3hg3bFPvkKkVbFDaMN', 'TransactionType': 'NFTokenMint',
 'fee': '10', 'sequence': 666082, 'flags': 0, 'last_ledger_sequence': 716371, 'signing_pub_key': '', 'TokenTaxon': 0, 'uri':
  '68747470733a2f2f697066732e696f2f697066732f6261666b72656967617036787a6a33337a34663732736c377163336262636b7371336b3236626a74657662746669763376706666637877637a6734'}, '
  origintype': 'EVENT_LIST', 'signmethod': 'BIOMETRIC', 'created_at': '2022-02-08T18:14:59Z',
  'expires_at': '2022-02-09T18:14:59Z', 'expires_in_seconds': 86163},
  'response': {'hex': '120019228000000024000AF251201B000AF342202A0000000068400000000000000F7321022073E020541E943226566AEE58830C75D0DD3683BE20313F8DB32E03F204E8257446304402202748E2ECCE4145271F592C51E7691BB32F0A4ED9D6F88C514915287B518CA073022043A5050BA89C136470F49981EA1C3B5DC5104B06ADE158E794AEABEE3162BE778114A5A487B09A8CD04B3C4E0B5F133BDFD52C19A435',
   'txid': '403EF4F8FF67566CD367050E2014A12FE8FA2CD185888393FD855B2C22897C37', 'resolved_at': '2022-02-08T18:16:19.000Z',
   'dispatched_to': '', 'dispatched_result': 'tesSUCCESS', 'dispatched_nodetype': 'CUSTOM', 'multisign_account': '',
    'account': 'rGaqbQwA2PFEQETV3hg3bFPvkKkVbFDaMN'}, 'custom_meta': {'identifier': None, 'blob': None, 'instruction': None}} """


""" {'meta': {'exists': True, 'uuid': '6e314cfb-3d31-4031-985b-ac6984a8cca4', 'multisign': False, 'submit': True, 'destination': '', 'resolved_destination': '', 'resolved': True, 'signed': True, 'cancelled': False, 'expired': False, 'pushed': True, 'app_opened': True, 'opened_by_deeplink': True, 'return_url_app': None, 'return_url_web': None, 'is_xapp': False}, 'application': {'name': 'xumm wallet nft markeplace intergration', 'description': 'xumm wallet integration for nft marketplace on xrpl', 'disabled': 0, 'uuidv4': '8c9c69e2-9e90-4ce5-92d5-1b379ff95777', 'icon_url': 'https://xumm-cdn.imgix.net/app-logo/f7e00f31-a3f7-40f0-91f5-7ff1b7bb2b5b.jpeg', 'issued_user_token': 'e5899868-642f-4680-9718-ba563af0c8ab'}, 'payload': {'tx_type': 'NFTokenMint', 'tx_destination': '', 'tx_destination_tag': None, 'request_json': {'account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8', 'TransactionType': 'NFTokenMint', 'fee': '10', 'sequence': 666082, 'flags': 0, 'last_ledger_sequence': 716371, 'signing_pub_key': '', 'TokenTaxon': 0, 'uri': '68747470733a2f2f697066732e696f2f697066732f6261666b72656967617036787a6a33337a34663732736c377163336262636b7371336b3236626a74657662746669763376706666637877637a6734'}, 'origintype': 'PUSH_NOTIFICATION', 'signmethod': 'BIOMETRIC', 'created_at': '2022-02-08T17:27:33Z', 'expires_at': '2022-02-09T17:27:33Z', 'expires_in_seconds': 86278}, 'response': {'hex': '120019228000000024000A29E3201B000AEF79202A0000000068400000000000000F732103DD699122D87D789ADAD5FF0521572BA28B3BAFBD77FE35F70CEB74D04DEE8B2B7447304502210083DCE6C8BE24C521A8847F46A61F9B2EEFAE002445FCF6A5A971B163D2CFEBFD0220415DBB00E545D8D2F252A413C41D39E874B2AF7D2D688893CD00F56BC761CB548114F7F917332EB18C40B065F37B729B4FB750A010D4', 'txid': 'D5A41F0E9D530E37CF1042651A7F24B595AED79E61844A0AE04BD6C26F6A61EF', 'resolved_at': '2022-02-08T17:27:44.000Z', 'dispatched_to': '', 'dispatched_result': 'tesSUCCESS', 'dispatched_nodetype': 'CUSTOM', 'multisign_account': '', 'account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8'}, 'custom_meta': {'identifier': None, 'blob': None, 'instruction': None}}
rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8 """


def store_user_token(id, user_token, account_address):
    """ utitlity function to store user token in database, get called by webhook route when signin payload received"""
    user = User.query.get(id)
    # TODO: store the expiration. 12 months expiration date.
    user.xumm_user_token = user_token
    user.xrp_account = account_address
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
