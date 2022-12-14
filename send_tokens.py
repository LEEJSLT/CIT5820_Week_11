#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
import algosdk

#Connect to Algorand node maintained by PureStake
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {
   "X-API-Key": algod_token,
}

acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

# generate the private key and address from account.generate_account()
def generate_account():
    private_key, address = algosdk.account.generate_account()
    print("private key:", private_key) # use run the test to get the private key
    print("address:", address) # use run the test to get the private key address
    return private_key, address

def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last

    # Your code here
    # private_key, address = generate_account()
    private_key = 'im0WgwifTg2IBvCJOKPMbN3tTgVFdJFgsx/3Daw59+/g0hN9ZMsHylMfohEKtdTChX/agpu5cYtxnGFFdIHHnA==' # using the generated private key as input
    address = '4DJBG7LEZMD4UUY7UIIQVNOUYKCX7WUCTO4XDC3RTRQUK5EBY6OB3CNRS4'  # using the generated address as input
    # mnemonic_secret = mnemonic.from_private_key(private_key) # generate the moemonic_secret
    # sk = mnemonic.to_private_key(mnemonic_secret)
    # pk = mnemonic.to_public_key(mnemonic_secret)

    sign = transaction.PaymentTxn(address,tx_fee,first_valid_round,last_valid_round,gen_hash,receiver_pk,tx_amount).sign(private_key) # sign the transaction with secret key
    txid = acl.send_transaction(sign)
    sender_pk = address # sign the address to sender_pk

    return sender_pk, txid


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo


if __name__ == "__generate_account__":
    generate_account()