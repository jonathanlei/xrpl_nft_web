import json
from xrpl.models.requests.account_info import AccountInfo
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo, NFTokenMint
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.clients import JsonRpcClient
from xrpl.utils import str_to_hex

# changed to websocket xls20 test net
print(str_to_hex("https://bafkreigap6xzj33z4f72sl7qc3bbcksq3k26bjtevbtfiv3vpffcxwczg4.ipfs.dweb.link/"))
client = JsonRpcClient("http://xls20-sandbox.rippletest.net:51234")
# get a test wallet
# test_wallet = generate_faucet_wallet(client)

test_wallet = Wallet.create()
print(test_wallet.classic_address)
breakpoint()
# create the transaction NFT TOKEN MINT
my_nft_mint = NFTokenMint(
    account=test_wallet.classic_address,
    token_taxon=0,
    uri=str_to_hex("https://bafkreigap6xzj33z4f72sl7qc3bbcksq3k26bjtevbtfiv3vpffcxwczg4.ipfs.dweb.link/")
)
my_tx_payment_signed = safe_sign_and_autofill_transaction(
    my_nft_mint, test_wallet, client)
# submit the transaction
tx_response = send_reliable_submission(my_tx_payment_signed, client)

print(tx_response)
""" 
minting flow: 
receiving info from FE: receiving wallet address, nft meta info,
question: do we mint for them on IPFS? 
    if we do: need media storage, seperate minting file
1. generate issuer account, sign
2. convert nft meta to hex, generate payment dict 
3. make payment obj and sign 


Params: 


 """


def mint_nfts(receiving_wallet, amount, nft_name, nft_uri, ):
    # TODO: convert amount of nft to be minted  to nft units
    # decide which type of data to be accepted, hexlified or no?
    issuer_account = generate_issuer_wallet()
    currency_amount = {
        "currency": binascii.hexlify(nft_name),
        "issuer": issuer_account,
        # values smaller than 70 zeros are considered NFTs (XLS14), "1000000000000000e-95" is 10
        "value": "1000000000000000e-96"
    }

    # set up trust line between receiving wallet and minter
    trust_set = TrustSet(
        account=receiving_wallet,
        fee="12",
        flags=131072,
        limit_amount=currency_amount)

    token_mint = NFTokenMint(
        token_taxon=1,
        issuer=issuer_account,
        uri=nft_uri
    )
    my_tx_payment = Payment(
        account=issuer_account,
        amount="1",
        destination=receiving_wallet,
        memos=nft_meta)
    # convert dict to Memo objs
    meta_data_memos = [Memo(memo_data=m["Memo"]["MemoData"], memo_format=m["Memo"]["MemoFormat"],
                            memo_type=m["Memo"]["MemoType"]) for m in nft_meta]
    # sign the transaction
    my_tx_payment_signed = safe_sign_and_autofill_transaction(
        my_tx_payment, issuer_wallet, client)

    tx_response = send_reliable_submission(my_tx_payment_signed, client)


# generate an one-off issuer wallet for minting, configure issuer account as well
# output issuer_account (address )
def generate_issuer_wallet():
    issuer_wallet = generate_faucet_wallet(client, debug=True)
    set_rippling_account = AccountSet(account=issuer_account,
                                      fee="12", flags=["8"])
    issuer_account = issuer_wallet.classic_address
    return issuer_account


# currency_amount = {
#     "currency": nft_meta[0]["MemoData"],
#     "issuer": issuer_account,
#     # values smaller than 70 zeros are considered NFTs (XLS14)
#     "value": "1000000000000000e-96"
# }
# # set up trust line between hot wallet and minter
# trust_set = TrustSet(
#     account=hot_wallet,
#     fee="12",
#     flags=131072,
#     limit_amount=currency_amount)

# # memos data containing nft meta data (description, URI to IPFS...)

# # convert dict to Memo objs
# meta_data_memos = [Memo(memo_data=m["Memo"]["MemoData"], memo_format=m["Memo"]["MemoFormat"],
#                         memo_type=m["Memo"]["MemoType"]) for m in meta_data]
# # make payment objs with memo data
# my_tx_payment = Payment(
#     account=issuer_account,
#     amount="1",
#     destination=hot_wallet,
#     memos=meta_data_memos)

# # sign the transaction
# my_tx_payment_signed = safe_sign_and_autofill_transaction(
#     my_tx_payment, issuer_wallet, client)


# tx_response = send_reliable_submission(my_tx_payment_signed, client)


# # query the ledger
# acct_info = AccountInfo(
#     account=hot_wallet,
#     ledger_index="validated",
#     strict=True,
# )
# response = client.request(acct_info)
# result = response.result
# print("response.status: ", response.status)
# print(json.dumps(response.result, indent=4, sort_keys=True))
