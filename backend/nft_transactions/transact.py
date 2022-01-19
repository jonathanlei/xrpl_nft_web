import json
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction, autofill
from xrpl.models.transactions import Payment, TrustSet, AccountSet, Memo, NFTokenCreateOffer, NFTokenMint, NFTokenCreateOfferFlag, NFTokenAcceptOffer
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.utils import str_to_hex, hex_to_str
from xrpl.models.amounts import IssuedCurrencyAmount

JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
client = JsonRpcClient("http://xls20-sandbox.rippletest.net:51234")

test_wallet = Wallet.create()
test_wallet_2 = Wallet.create()
print(test_wallet.classic_address, "1")
print(test_wallet_2.classic_address, "2")

# make transaction,request the wallet sign the transaction
# 1. populate the transaction - with wallet address
# 2. autofill? send to the wallet
# 3. xumm wallet sdk (~60%, or ledger nano, lesser used wallets)- or build a small client app with server,key on it 

breakpoint()
# TODO: figure out a way to auto faucet the accounts, right now have to manually fund it
# create the transaction NFT TOKEN MINT
my_nft_mint = NFTokenMint(
    account=test_wallet.classic_address,
    token_taxon=0,
    uri=str_to_hex(
        "https://bafkreigap6xzj33z4f72sl7qc3bbcksq3k26bjtevbtfiv3vpffcxwczg4.ipfs.dweb.link/"),
)
# TODO: seperate autofill and sign (request for the client to sign)

my_tx_payment_filled = autofill(my_nft_mint, client)
breakpoint()

my_tx_payment_signed = safe_sign_and_autofill_transaction(
    my_nft_mint, test_wallet, client)
# submit the transaction
tx_response = send_reliable_submission(my_tx_payment_signed, client)
"""
sending and receiving NFTs via XRPL
"""
# TODO: sending payment from receiver_wallet
buyer = test_wallet_2.classic_address

token_id = ""
try:
    token_id = tx_response.result["meta"]["AffectedNodes"][1]['CreatedNode'][
        'NewFields']['NonFungibleTokens'][0]['NonFungibleToken']['TokenID']
except KeyError:
    token_id = tx_response.result["meta"]["AffectedNodes"][0]['CreatedNode'][
        'NewFields']['NonFungibleTokens'][0]['NonFungibleToken']['TokenID']
sell_flag = NFTokenCreateOfferFlag(1)
# create offer 
my_nft_offer = NFTokenCreateOffer(
    account=test_wallet.classic_address,
    destination=buyer,
    amount="1000000000c",
    token_id=token_id,
    flags=[sell_flag]
)
my_tx_offer_signed = safe_sign_and_autofill_transaction(
    my_nft_offer, test_wallet, client)

# submit the transaction
tx_offer_response = send_reliable_submission(my_tx_offer_signed, client)

#submit offer 
sell_offer_id = ""

affected_nodes = tx_offer_response.result["meta"]["AffectedNodes"]
for node in affected_nodes: 
    if 'CreatedNode' in node:
        if node['CreatedNode']['LedgerEntryType'] == "NFTokenOffer":
            sell_offer_id = node['CreatedNode']['LedgerIndex']
            break
my_nft_accept_offer = NFTokenAcceptOffer(
    account=test_wallet_2.classic_address,
    sell_offer=sell_offer_id,
)
my_tx_offer_accepted_signed = safe_sign_and_autofill_transaction(
    my_nft_accept_offer, test_wallet_2, client)


# submit the transaction
tx_offer_accepted_response = send_reliable_submission(my_tx_offer_accepted_signed, client)
print(tx_offer_accepted_response)

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




