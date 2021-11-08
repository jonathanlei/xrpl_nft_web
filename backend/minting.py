import json
from xrpl.models.requests.account_info import AccountInfo
from xrpl.transaction import send_reliable_submission
from xrpl.transaction import safe_sign_and_autofill_transaction
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo
from xrpl.wallet import generate_faucet_wallet
from xrpl.clients import JsonRpcClient
import binascii
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient(JSON_RPC_URL)


""" 
flow: 
receiving info from FE: receiving wallet address, nft meta info,
question: do we mint for them on IPFS? 
    if we do: media storage, seperate minting py
1. generate issuer account, sign
2. convert nft meta to hex, generate payment dict 
3. make payment obj and sign 
 """
def minting(receiving_wallet, amount, nft_meta, ):
    issuer_account = generate_issuer_wallet()



# generate an one-off issuer wallet for minting, configure issuer account as well
# output issuer_account (address )
def generate_issuer_wallet():
    issuer_wallet = generate_faucet_wallet(client, debug=True)
    set_rippling_account = AccountSet(account=issuer_account,
                                  fee="12", flags=["8"])
    issuer_account = issuer_wallet.classic_address
    return issuer_account


def hex_convertor(string):
    return binascii.hexlify(string)

# generate test wallets from testnet
test_wallet = generate_faucet_wallet(client, debug=True)

# issuer wallet
issuer_wallet = generate_faucet_wallet(client, debug=True)

# wallet receiving the mint
hot_wallet = test_wallet.classic_address

issuer_account = issuer_wallet.classic_address

# set minter account flags to connect to rippling
set_rippling_account = AccountSet(account=issuer_account,
                                  fee="12", flags=["8"])


currency_amount = {
    # HEX ecoding of nft name
    # TODO:HEX name convertor
    "currency": "64656E6163687477616368740000000000000000",
    "issuer": issuer_account,
    # values smaller than 70 zeros are considered NFTs (XLS14)
    "value": "1000000000000000e-96"
}
# set up trust line between hot wallet and minter
trust_set = TrustSet(
    account=hot_wallet,
    fee="12",
    flags=131072,
    limit_amount=currency_amount)

# memos data containing nft meta data (name, URI to IPFS...)
meta_data = [{
    "Memo": {
        # description
        "MemoData": "546861742773206F6E6520736D616C6C20696D616765206F66206D6F6F6E2C206F6E65206769616E74206C65617020666F72204E4654206F6E20746865205852504C",
        "MemoFormat": "746578742F706C61696E",
        "MemoType": "6E66742F30"
    }
},
    {
    "Memo": {
        # arthur
        "MemoData": "48756265727420476574726F7577",
        "MemoFormat": "746578742F706C61696E",
        "MemoType": "6E66742F31"
    }
},
    {
    "Memo": {
        # primary URI
        "MemoData": "697066733A2F2F62616679626569686561786B696A3276656D6B7337726B716E6F67367933367579793337626B33346D697533776F72636A756F6833747532773279",
        "MemoFormat": "746578742F757269",
        "MemoType": "6E66742F32"
    }
},

    {
    "Memo": {
        # secondary URI
        "MemoData": "68747470733A2F2F676574726F75772E636F6D2F696D672F707572706C656D6F6F6E2E706E67",
        "MemoFormat": "746578742F757269",
        "MemoType": "6E66742F33"
    }
},
    {
    "Memo": {
        # reduced image data
        "MemoData": "646174613A696D6167652F6769663B6261736536342C52306C474F446C684641415541505141414141414142415145434167494441774D4542415146425155474267594842776348392F66342B506A352B666E362B7672372B2F76382F507A392F66332B2F76377741414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414143483542414541414241414C4141414141415541425141414157524943534F5A476D65614B7175624F74437A664D7551564D456937674D41494D554D684942554F4D784941454141544A736942674F4A674267654267456A476E413063673945524446464342364E4D6248305945684543454579784844414354316571383352486C69654D73474147414641414949436A495051776F4F66675A4A41544A5A5932414C4255634B535A516A684552424A41384355774F6750414B6649326445547156554A6A774166364345435352694F436F4D42416F6A6A61675149514137",
        "MemoFormat": "746578742F757269",
        "MemoType": "6E66742F34"
    }
}]
# convert dict to Memo objs
meta_data_memos = [Memo(memo_data=m["Memo"]["MemoData"], memo_format=m["Memo"]["MemoFormat"],
                        memo_type=m["Memo"]["MemoType"]) for m in meta_data]
# make payment objs with memo data
my_tx_payment = Payment(
    account=issuer_account,
    amount="1",
    destination=hot_wallet,
    memos=meta_data_memos)

# sign the transaction
my_tx_payment_signed = safe_sign_and_autofill_transaction(
    my_tx_payment, issuer_wallet, client)


tx_response = send_reliable_submission(my_tx_payment_signed, client)


# query the ledger
acct_info = AccountInfo(
    account=hot_wallet,
    ledger_index="validated",
    strict=True,
)
response = client.request(acct_info)
result = response.result
print("response.status: ", response.status)
print(json.dumps(response.result, indent=4, sort_keys=True))
