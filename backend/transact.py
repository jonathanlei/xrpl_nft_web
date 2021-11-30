import json
from xrpl.models.requests.account_info import AccountInfo
from xrpl.transaction import send_reliable_submission
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo
from xrpl.clients import JsonRpcClient
import binascii
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)

"""
sending and receiving NFTs via XRPL 
"""
#TODO: sending payment from receiver_wallet

def send_nft(sender_wallet, receiver_wallet, amount, nft_name):
    currency_amount = {
        "currency": binascii.hexlify(nft_name),
        "issuer": sender_wallet,
        # values smaller than 70 zeros are considered NFTs (XLS14), "1000000000000000e-95" is 10
        "value": "1000000000000000e-96"
    }
    #set up trust set
    trust_set = TrustSet(
        account=receiving_wallet,
        fee="12",
        flags=131072,
        limit_amount=currency_amount)
    # Make payment to send the currency
    tx_payment = Payment(
        account=sender_wallet,
        amount=amount,
        destination=receiver_wallet,
        memos=nft_name)
    tx_payment_signed = safe_sign_and_autofill_transaction(
        tx_payment, sender_wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)
