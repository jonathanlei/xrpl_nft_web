import json
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction, autofill, get_transaction_from_hash, transaction_json_to_binary_codec_form
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo, NFTokenCreateOffer, NFTokenMint, NFTokenCreateOfferFlag, NFTokenAcceptOffer
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.utils import str_to_hex, hex_to_str
from xrpl.models.amounts import IssuedCurrencyAmount
import datetime
from models import User, Auction
from .xumm import sign_transactions, get_transaction_id
import os
from dotenv import load_dotenv

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient("http://xls20-sandbox.rippletest.net:51234")
load_dotenv()

central_wallet = Wallet(sequence=int(os.getenv(
    "CENTRAL_WALLET_SEQUENCE")), seed=os.getenv("CENTRAL_WALLET_SEED"))
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


def mintNft(xrp_account, img_url, nft_meta):
    
    user = User.query.get(xrp_account)
    # create token mint object
    my_nft_mint = NFTokenMint(
        account=user.xrp_account,
        token_taxon=0,
        uri=str_to_hex(img_url)
    )
    # TODO: test this
    tx_payment_filled = autofill(my_nft_mint, client).to_xrpl()
    nft_meta["uri"] = img_url
    custom_meta = {'blob': nft_meta, "instruction": "mint_nft"}
    # {"pushed": True} or {"png_url": "..."} depending on the push status
    result = sign_transactions(
        tx_payment_filled, user.xumm_user_token, custom_meta)
    print(result, "RESULT FOR MINTING NFT REQUEST")
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


def get_offer_id(payload_id):
    transaction_hash = get_transaction_id(payload_id)
    meta = get_transaction_dict(transaction_hash)
    offer_id = None
    for node in meta["AffectedNodes"]:
        if "CreatedNode" in node:
            if node["CreatedNode"]["LedgerEntryType"] == "NFTokenOffer":
                offer_id = node["CreatedNode"]["LedgerIndex"]
                break
    return offer_id
# print(get_offer_id("43993fc3-4587-44e0-9bc6-8365074d8587"))


def get_nft_id(payload_id):
    """ get nft_token_id from minting payload """
    transaction_hash = get_transaction_id(payload_id)
    meta = get_transaction_dict(transaction_hash)
    #TODO: check if the transaction is applied/valid 
        # alternative: python websocket - subscribe to ledger 
        # enqueue a job in the job queue, check again on the status of the transaction - has it been validated (go through the conditions), loop through jobs 
        
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
#         "https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg")
# )
# tx_payment_filled = autofill(my_nft_mint, client)
# tx_payment_filled = transaction_json_to_binary_codec_form(
#     tx_payment_filled.to_dict())
# custom_meta = {'blob':{"user_id":1},"instruction": "mint_nft"}
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
# TODO: set expirations date of offer. and look into how to cancel (NFTokenCancel)
# TODO: have buy/sell offer on chain for bids.
# TODO: test the reserve for the offer amount.


def createNftBuyOffer(auction_id, buyer_xrp_account, amount, brokered_mode=True, seller_id=None):
    buyer = User.query.get(buyer_xrp_account)
    owner_address = None
    if brokered_mode:
        owner_address = central_wallet.classic_address
    else:
        owner_address = User.query.get(seller_id).xrp_account
    token_id = Auction.query.get(auction_id).nft_id
    # any other flag than 1 is buy, 1 is sell
    nft_offer = NFTokenCreateOffer(
        account=buyer_xrp_account,
        owner=owner_address,
        amount=amount,
        token_id=token_id,
        # TODO: test if flag works
    )
    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(nft_offer, client).to_dict())
    custom_meta = {
        "blob": {"buyer_xrp_account": buyer_xrp_account,
                 "auction_id": auction_id,
                 "price": amount},
        "instruction": "create_buy_offer"}
    result = sign_transactions(
        tx_offer_filled, buyer.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result

# # trying sell offer
# sell_flag = NFTokenCreateOfferFlag(1)
# tokenId = "00000000F7F917332EB18C40B065F37B729B4FB750A010D48542EAAC00000011"
# nft_offer = NFTokenCreateOffer(
#     account="rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8",
#     destination="rGaqbQwA2PFEQETV3hg3bFPvkKkVbFDaMN",
#     amount="1",
#     token_id=tokenId,
#     flags=[sell_flag],
# )
# tx_offer_filled = autofill(nft_offer, client)
# tx_offer_filled = transaction_json_to_binary_codec_form(
#         tx_offer_filled.to_dict())
# sign_transactions(tx_offer_filled, "e5899868-642f-4680-9718-ba563af0c8ab",{})


# trying buy offer

# tokenId = "00000000F7F917332EB18C40B065F37B729B4FB750A010D412C5D5A70000000C"
# nft_offer = NFTokenCreateOffer(
#     account="rGaqbQwA2PFEQETV3hg3bFPvkKkVbFDaMN",
#     owner="rPcwJW3BQ7JZ4VNARFWFQudwG45he2vaS8",
#     amount="1",
#     token_id=tokenId,
# )
# tx_offer_filled = autofill(nft_offer, client)
# tx_offer_filled = transaction_json_to_binary_codec_form(
#         tx_offer_filled.to_dict())
# print("created offer")
# sign_transactions(tx_offer_filled, "e3bf2a28-a7c7-421a-a1c5-4c86b806551b",{})
# # sell_offer_id = 398AAA98324AB8C4C69E63D480BB66F2164329306FD9397CACC54EC4F48C339B


def createNftSellOffer(auction_id, seller_xrp_account, amount,
                       brokered_mode=True, buyer_xrp_account=None):
    # TODO: create a central wallet for buyer
    buyer_address = None
    if brokered_mode:
        buyer_address = central_wallet.classic_address
    else:
        buyer_address = User.query.get(buyer_xrp_account).xrp_account
    token_id = Auction.query.get(auction_id).nft_id
    seller = User.query.get(seller_xrp_account)
    sell_flag = NFTokenCreateOfferFlag(1)
    nft_offer = NFTokenCreateOffer(
        account=seller.xrp_account,
        destination=buyer_address,
        amount=amount,
        token_id=token_id,
        flags=[sell_flag],
    )
    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(nft_offer, client).to_dict())
    custom_meta = {
        "blob": {"seller": seller_xrp_account, "auction_id": auction_id}, "instruction": "create_sell_offer"}
    result = sign_transactions(
        tx_offer_filled, seller.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result

    # submit the transaction


def createAcceptOffer(offer_id, destination_xrp_account, isSell):
    user = User.query.get(destination_xrp_account)
    nft_accept_offer = None
    if isSell:
        nft_accept_offer = NFTokenAcceptOffer(
            account=destination_xrp_account,
            sell_offer=offer_id,
        )
    else:
        nft_accept_offer = NFTokenAcceptOffer(
            account=destination_xrp_account,
            buy_offer=offer_id,
        )
    tx_offer_filled = autofill(nft_accept_offer, client)
    tx_offer_filled = transaction_json_to_binary_codec_form(
        autofill(tx_offer_filled, client).to_dict())
    custom_meta = {
        "blob": {"offer_id": offer_id}, "instruction": "create_accept_offer"}
    result = sign_transactions(
        tx_offer_filled, user.xumm_user_token, custom_meta)
    if "pushed" in result:
        return result
    else:
        result["pushed"] = False
        return result


def createAcceptOfferAndSign(auction_id, sell_offer_id):
    """ accept sell offer after the auction ending from central wallet"""
    highest_buy_offer = Auction.query.get(auction_id).highest_offer_id
    nft_accept_offer = NFTokenAcceptOffer(
        account=central_wallet.classic_address,
        sell_offer=sell_offer_id,
        buy_offer=highest_buy_offer
    )
    my_tx_payment_signed = safe_sign_and_autofill_transaction(
        nft_accept_offer, central_wallet, client)
    tx_response = send_reliable_submission(my_tx_payment_signed, client)
    return tx_response


# nft_offer = NFTokenAcceptOffer(
#     account="rGaqbQwA2PFEQETV3hg3bFPvkKkVbFDaMN",
#     sell_offer="499B436399FAC5CE9FBE603D16BC8401ADA235E7FCCE3B913980A4B4097D026C"
# )
# tx_offer_filled = autofill(nft_offer, client)
# tx_offer_filled = transaction_json_to_binary_codec_form(
#     tx_offer_filled.to_dict())
# custom_meta = {"instruction": "nft_buy_offer", "blob": {}}
# sign_transactions(
#     tx_offer_filled, "e3bf2a28-a7c7-421a-a1c5-4c86b806551b", custom_meta)
