import json
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction, autofill, get_transaction_from_hash, transaction_json_to_binary_codec_form
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo, NFTokenCreateOffer, NFTokenMint, NFTokenCreateOfferFlag, NFTokenAcceptOffer
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.utils import str_to_hex, hex_to_str
from xrpl.models.amounts import IssuedCurrencyAmount
import requests
import datetime
# from models import User
from .xumm import sign_transactions, get_transaction_id

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient("http://xls20-sandbox.rippletest.net:51234")

# url = "http://xls20-sandbox.rippletest.net:51234"
# "AD9825BC11FB54DA3E5DBE911E4F5F4B0208ADFB7FA677BB60DB9971964B79C1"
# response = requests.post(url, data={"method": "tx", "params": [{"transaction": "AD9825BC11FB54DA3E5DBE911E4F5F4B0208ADFB7FA677BB60DB9971964B79C1"}]})
# breakpoint()
# make dtransaction,request the wallet sign the transaction
# 1. populate the transaction - with wallet address
# 2. autofill? send to the wallet
# 3. xumm wallet sdk (~60%, or ledger nano, lesser used wallets)- or build a small client app with server,key on it
# TODO: figure out a way to auto faucet the accounts, right now have to manually fund it
# create the transaction NFT TOKEN MINT


def mintNft(id, img_url):
    user = User.query.get(id)
    # create token mint object
    my_nft_mint = NFTokenMint(
        account=user.xrp_account_id,
        token_taxon=0,
        uri=str_to_hex(img_url)
    )
    # TODO: test this
    tx_payment_filled = autofill(my_nft_mint, client).to_xrpl()
    custom_meta = {"identifier": id, "instruction": "mint_nft"}
    # {"pushed": True} or {"png_url": "..."} depending on the push status
    result = sign_transactions(
        tx_payment_filled, user.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result
    # TODO: get and store nft token ID?


def get_transaction_dict(txid):
    """ reponse = get_transaction_from_hash(
    "71ECA5C1D9145507EE022E363197F2621A8E8784E98E8F13A1EA5CED92C7691F", client) """
    response = get_transaction_from_hash(txid, client)
    return response.result['meta']


def get_nft_id(payload_id):
    transaction_hash = get_transaction_id(payload_id)
    meta = get_transaction_dict(transaction_hash)
    relevant_nodes = meta['AffectedNodes']
    nft_toke_page = None
    for node in relevant_nodes:
        if "CreatedNode" in node:
            if node["CreatedNode"]["LedgerEntryType"] == "NonFungibleTokens":
                nft_toke_page = node["CreatedNode"]
        elif "ModifiedNode" in node:
            if node["ModifiedNode"]["LedgerEntryType"] == "NFTokenPage":
                nft_toke_page = node["ModifiedNode"]
    if "PreviousFields" in nft_toke_page:
        previousFields = nft_toke_page["PreviousFields"]
        if "NonFungibleTokens" in previousFields:
            # might have to check the two keys
            previous_token_ids = [token["NonFungibleToken"]["TokenID"]
                                  for token in previousFields["NonFungibleTokens"]]
    previous_token_id_set = set(previous_token_ids)
    final_token_ids = []
    final_tokens = None
    if "FinalFields" in nft_toke_page:
        final_tokens = nft_toke_page["FinalFields"]
    elif "NewFields" in nft_toke_page:
        final_tokens = nft_toke_page["NewFields"]
    if "NonFungibleTokens" in final_tokens:
        final_token_ids = [token["NonFungibleToken"]["TokenID"]
                           for token in final_tokens["NonFungibleTokens"]]

    token_id = list(filter(
        lambda final_token_ids: final_token_ids not in previous_token_id_set, final_token_ids))[0]
    # TODO: make sure token_id is stored
    return token_id


# my_nft_mint = NFTokenMint(
#     account="rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8",
#     token_taxon=0,
#     uri=str_to_hex(
#         "https://images.livemint.com/img/2022/02/14/1600x900/NFT_1644804887471_1644804887655.jpg")
# )
# tx_payment_filled = autofill(my_nft_mint, client)
# tx_payment_filled = transaction_json_to_binary_codec_form(
#     tx_payment_filled.to_dict())
# custom_meta = {"identifier": 1, "instruction": "mint_nft"}
# sign_transactions(tx_payment_filled,
#                   "e5899868-642f-4680-9718-ba563af0c8ab", custom_meta)


# asih token : 608e97e9-6b22-43e5-8580-e1712ede505a
# {'Account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8', 'Fee': '10', 'Flags': 2147483648, 'LastLedgerSequence': 923674, 'Sequence': 666099, 'SigningPubKey': '03DD699122D87D789ADAD5FF0521572BA28B3BAFBD77FE35F70CEB74D04DEE8B2B', 'TokenTaxon': 0, 'TransactionType': 'NFTokenMint',
#  'TxnSignature': '30440220162C0D00CC26D01744A84D32835A5E2A2CD553A150D3E94C9B572480C22B89D602202A01F5B5C04081722D9F35BBA70E2EDC8F416EE5523528FF6C221881F805E691',
#  'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734',
#  'date': 698279591, 'hash': '71ECA5C1D9145507EE022E363197F2621A8E8784E98E8F13A1EA5CED92C7691F', 'inLedger': 923660, 'ledger_index': 923660, 'meta': {'AffectedNodes': [{'ModifiedNode': {'FinalFields': {'Account': 'rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8', 'Balance': '989999785', 'Flags': 0, 'MintedTokens': 11, 'OwnerCount': 8, 'Sequence': 666100}, 'LedgerEntryType': 'AccountRoot', 'LedgerIndex': '7FBDFE631F9102BEEBA03D3FEF0C556A1A0315EBFF06F113C24CB6EFE1AC6157', 'PreviousFields': {'Balance': '989999795', 'MintedTokens': 10, 'Sequence': 666099}, 'PreviousTxnID': 'C8891B82C79361C81C1968FC76ACCB8F8BDEA8069A2BEF02976EE67F750B6604', 'PreviousTxnLgrSeq': 917659}}, {'ModifiedNode': {'FinalFields': {'Flags': 0, 'NonFungibleTokens': [{'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D40000099B00000000'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D416E5DA9C00000001'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D42DCBAB9D00000002'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D444B17C9E00000003', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D45B974D9F00000004', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4727D1EA000000005', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D48962EFA100000006', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4A048C0A200000007', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4B72E91A300000008', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {
#      'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4CE1462A400000009', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4E4FA33A50000000A', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}]}, 'LedgerEntryType': 'NFTokenPage', 'LedgerIndex': 'F7F917332EB18C40B065F37B729B4FB750A010D4FFFFFFFFFFFFFFFFFFFFFFFF', 'PreviousFields': {'NonFungibleTokens': [{'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D40000099B00000000'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D416E5DA9C00000001'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D42DCBAB9D00000002'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D444B17C9E00000003', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D45B974D9F00000004', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4727D1EA000000005', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D48962EFA100000006', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4A048C0A200000007', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4B72E91A300000008', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}, {'NonFungibleToken': {'TokenID': '00000000F7F917332EB18C40B065F37B729B4FB750A010D4CE1462A400000009', 'URI': '68747470733A2F2F697066732E696F2F697066732F6261666B72656967617036787A6A33337A34663732736C377163336262636B7371336B3236626A74657662746669763376706666637877637A6734'}}]}, 'PreviousTxnID': 'C8891B82C79361C81C1968FC76ACCB8F8BDEA8069A2BEF02976EE67F750B6604', 'PreviousTxnLgrSeq': 917659}}], 'TransactionIndex': 0, 'TransactionResult': 'tesSUCCESS'}, 'validated': True}
# reponse.result['meta']['AffectedNodes'][1]['ModifiedNode'][']
# other wallet token id "e3bf2a28-a7c7-421a-a1c5-4c86b806551b"
# submit the transaction
# tx_response = send_reliable_submission(my_tx_payment_signed, client)
"""
sending and receiving NFTs via XRPL
"""
# # TODO: sending payment from receiver_wallet
# buyer = test_wallet_2.classic_address

# token_id = ""
# try:
#     token_id = tx_response.result["meta"]["AffectedNodes"][1]['CreatedNode'][
#         'NewFields']['NonFungibleTokens'][0]['NonFungibleToken']['TokenID']
# except KeyError:
#     token_id = tx_response.result["meta"]["AffectedNodes"][0]['CreatedNode'][
#         'NewFields']['NonFungibleTokens'][0]['NonFungibleToken']['TokenID']

# TODO: verify the user own the account and have the reserve, check public key hashes to address.

# issue:
# rely on two different people to authorize - no direct control over the transaction.

# TODO: set expirations date of offer. and look into how to cancel (NFTokenCancel)
# TODO: have buy/sell offer on chain for bids.
# TODO: test the reserve for the offer amount.


def createNftBuyOffer(auction_id, seller_id, buyer_id, token_id, amount):
    buyer = User.query.get(buyer_id)
    seller = User.query.get(seller_id)
    # any other flag than 1 is buy, 1 is sell
    nft_offer = NFTokenCreateOffer(
        account=buyer.xrp_account_id,
        destination=seller.xrp_account_id,
        amount=amount,
        token_id=token_id,
        # TODO: test if flag works
    )

    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(nft_offer, client).to_dict())
    custom_meta = {
        "identifier": f"buyer: {buyer_id}, signed_time: {datetime.now()}, auction: {auction_id}", "instruction": "create_buy_offer"}
    result = sign_transactions(
        tx_offer_filled, buyer.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result

 # TODO: try no flag and test buy offer
# sell_flag = NFTokenCreateOfferFlag(1)
# tokenId = "00000000F7F917332EB18C40B065F37B729B4FB750A010D40000099B00000000"
# nft_offer = NFTokenCreateOffer(
#     account="rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8",
#     destination="r9jcocVzhfkH5PvgasDPhtde3zPVE2zDBK",
#     amount="1",
#     token_id=tokenId,
#     flags=[sell_flag],
# )
# tx_offer_filled = autofill(nft_offer, client)
# tx_offer_filled = transaction_json_to_binary_codec_form(
#         tx_offer_filled.to_dict())
# sign_transactions(tx_offer_filled, "e5899868-642f-4680-9718-ba563af0c8ab")


def createNftSellOffer(seller_id, buyer_id, token_id, amount):
    buyer = User.query.get(buyer_id)
    seller = User.query.get(seller_id)
    # TODO: look into more flags and functionalities
    sell_flag = NFTokenCreateOfferFlag(1)
    nft_offer = NFTokenCreateOffer(
        account=seller.xrp_account_id,
        destination=buyer.xrp_account_id,
        amount=amount,
        token_id=token_id,
        flags=[sell_flag],
    )
    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(nft_offer, client).to_dict())
    custom_meta = {
        "identifier": buyer_id, "instruction": "create_sell_offer"}
    result = sign_transactions(
        tx_offer_filled, seller.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result

    # submit the transaction

# # submit offer
# sell_offer_id = ""


# affected_nodes = tx_offer_response.result["meta"]["AffectedNodes"]
# for node in affected_nodes:
#     if 'CreatedNode' in node:
#         if node['CreatedNode']['LedgerEntryType'] == "NFTokenOffer":
#             sell_offer_id = node['CreatedNode']['LedgerIndex']
#             break


def createAcceptOffer(offer_id, destination_user_id, isSell):
    user = User.query.get(destination_user_id)
    nft_accept_offer = None
    if isSell:
        nft_accept_offer = NFTokenAcceptOffer(
            account=user.xrp_account_id,
            sell_offer=offer_id,
        )
    else:
        nft_accept_offer = NFTokenAcceptOffer(
            account=user.xrp_account_id,
            buy_offer=offer_id,
        )
    tx_offer_filled = autofill(nft_accept_offer, client)
    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(tx_offer_filled, client).to_dict())
    custom_meta = {
        "identifier": offer_id, "instruction": "create_accept_offer"}
    result = sign_transactions(
        tx_offer_filled, buyer.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result

# TODO: cancel offer

# my_tx_offer_accepted_signed = safe_sign_and_autofill_transaction(
#     my_nft_accept_offer, test_wallet_2, client)


# # submit the transaction
# tx_offer_accepted_response = send_reliable_submission(
#     my_tx_offer_accepted_signed, client)
# print(tx_offer_accepted_response)

# def send_nft(sender_wallet, receiver_wallet, amount, nft_name):
#     currency_amount = {
#         "currency": binascii.hexlify(nft_name),
#         "issuer": sender_wallet,
#         # values smaller than 70 zeros are considered NFTs (XLS14), "1000000000000000e-95" is 10
#         "value": "1000000000000000e-96"
#     }
#     # set up trust set
#     trust_set = TrustSet(
#         account=receiving_wallet,
#         fee="12",
#         flags=131072,
#         limit_amount=currency_amount)
#     # Make payment to send the currency
#     tx_payment = Payment(
#         account=sender_wallet,
#         amount=amount,
#         destination=receiver_wallet,
#         memos=nft_name)
#     tx_payment_signed = safe_sign_and_autofill_transaction(
#         tx_payment, sender_wallet, client)
#     tx_response = send_reliable_submission(my_tx_payment_signed, client)


result = {'Account': 'rMSLSHbmJ6QbWtGGiUGQr5eKNJs7cz3WVA',
          'Amount': '100', 'Destination': 'rKjZpLYqJzjb3ziNVfL3AVkracbAK4HRAT',
          'Fee': '10', 'Flags': 1, 'LastLedgerSequence': 1402668, 'Sequence': 1402640,
          'SigningPubKey': 'ED5D356242B72EB1CC8E94A4A244B61B2C6CC55A996D7CD2CBD00CB66C36F2D5E8',
          'TokenID': '00000000E02D2398C90E04EFEEA995C206CA26810F73D5560000099B00000000',
          'TransactionType': 'NFTokenCreateOffer', 'TxnSignature': 'C8478B1D3CBD4CDC82D6DEE88F6D05012D7C9B22C3A4B9545186E584A66691691123DD699791A06B4E41A925B39E13F41B1D1507B9840819412D9DC9F989EA06', 'date': 693961741, 'hash': '678A197364391540FE938B609F9666ED29277C210B8C292E7D84959CC4ACFDAD', 'inLedger': 1402650, 'ledger_index': 1402650,
          'meta': {'AffectedNodes': [{'ModifiedNode': {'LedgerEntryType': 'AccountRoot', 'LedgerIndex': '2CBE8D81337E42235DFBE5C2E1FE5AB6CCFDFD2531230E15D8137480E6920C43',
                                                       'PreviousTxnID': '26176DC2E51DDB1EB3084C571A0966859289DF6E6DEB8BB4B6DCF7DDF0E25D0D', 'PreviousTxnLgrSeq': 1396325}},
                                     {'ModifiedNode': {'FinalFields': {'Account': 'rMSLSHbmJ6QbWtGGiUGQr5eKNJs7cz3WVA',
                                                                       'Balance': '999999980', 'Flags': 0, 'MintedTokens': 1, 'OwnerCount': 2, 'Sequence': 1402641}, 'LedgerEntryType': 'AccountRoot', 'LedgerIndex': '375D28248B03462978E3F4CEEECD8182689142B82DD84A8489BE75BAF5777979', 'PreviousFields': {
                                         'Balance': '999999990', 'OwnerCount': 1, 'Sequence': 1402640}, 'PreviousTxnID': '439BC3C38B0E4085867235FAD136E86CD157206D4947BC030D378FB6F242C472', 'PreviousTxnLgrSeq': 1402644}},
                                     {'CreatedNode': {'LedgerEntryType': 'NFTokenOffer',
                                                      'LedgerIndex': '65DAB58BB31FA8BF0095A7A2C84B078967D32B914C759923DB2F392ED7B34112',
                                                      'NewFields': {'Amount': '100', 'Destination': 'rKjZpLYqJzjb3ziNVfL3AVkracbAK4HRAT', 'Flags': 1,
                                                                    'Owner': 'rMSLSHbmJ6QbWtGGiUGQr5eKNJs7cz3WVA', 'TokenID': '00000000E02D2398C90E04EFEEA995C206CA26810F73D5560000099B00000000'}}},
                                     {'CreatedNode': {'LedgerEntryType': 'DirectoryNode', 'LedgerIndex': '7C4AA035D66A99CBD7A22320A9E4DC3F1663ADC4A4B2DB031CC4659E1F3CD158',
                                                      'NewFields': {'Flags': 2, 'RootIndex': '7C4AA035D66A99CBD7A22320A9E4DC3F1663ADC4A4B2DB031CC4659E1F3CD158',
                                                                    'TokenID': '00000000E02D2398C90E04EFEEA995C206CA26810F73D5560000099B00000000'}}},
                                     {'CreatedNode': {'LedgerEntryType': 'DirectoryNode', 'LedgerIndex': 'BDA4C05E1E8C0BAC3A45DA603660715921FDE950354DBCC9B6A9B1CD4CDC1936',
                                                      'NewFields': {'Owner': 'rMSLSHbmJ6QbWtGGiUGQr5eKNJs7cz3WVA', 'RootIndex': 'BDA4C05E1E8C0BAC3A45DA603660715921FDE950354DBCC9B6A9B1CD4CDC1936'}}}], 'TransactionIndex': 0, 'TransactionResult': 'tesSUCCESS'}, 'validated': True}
