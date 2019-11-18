import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
#from models import Contract, User
#from flask_login import current_user

# web3.py instanciado
w3 = Web3(HTTPProvider(" https://ropsten.infura.io/caf17ea0064344db8f7b2eb3a67bb058 "))


#key= "0xFF1AFD0E33BB5854CBDCE5982806D6B58831FC568F77A3D0FEEDCA85E948CA35"
#acct = w3.eth.account.privateKeyToAccount(key)

# Compila tu contrato inteligente en truffle.
truffleFile = json.load(open('./build/contracts/SalesContract.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract= w3.eth.contract(bytecode=bytecode, abi=abi)

#creacion del contrato
def newContract(description, price, key):
    acct = w3.eth.account.privateKeyToAccount(key)
    construct_txn = contract.constructor(str(description), int(price)).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')})

    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contracto_a = tx_receipt['contractAddress']
    return contracto_a

def movementHash (tx, key):
    signed_tx = w3.eth.account.signTransaction(tx, key)
    tx_hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt


