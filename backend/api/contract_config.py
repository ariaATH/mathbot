from .web3_config_payment import address_node ,w3 , contract , OWNER_ADDRESS , PRIVATE_KEY
import json
from dotenv import load_dotenv
import os

contract_address = address_node.to_checksum_address("write address")
contract_abi = json.loads('ABI')
owner_address = address_node.to_checksum_address(OWNER_ADDRESS)
nonce_owner = w3.eth.get_transaction_count(owner_address)

def Createcomp(ID , Price):
    tx = contract.functions.Addcomp(ID , Price).build_transaction({
        'from':owner_address ,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce_owner
    })
    sign_tx = w3.eth.account.sign_transaction(tx , PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def Createcompfree(ID):
    tx = contract.functions.Addfreecomp(ID).build_transaction({
        'from':owner_address ,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce_owner
    })
    sign_tx = w3.eth.account.sign_transaction(tx , PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def Awardwinners(address_1 , address_2 , address_3 , ID ):
    tx = contract.functions.Awardwinners(address_1 , address_2 , address_3 , ID ).build_transaction({
        'from':owner_address ,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce_owner
    })
    sign_tx = w3.eth.account.sign_transaction(tx , PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def AwardWithPercentage(address_1 , address_2 , address_3 ,percent_1 , percent_2 , percent_3 , ID ):
    tx = contract.functions.Awardwinners(address_1 , address_2 , address_3 ,percent_1 , percent_2 , percent_3 , ID ).build_transaction({
        'from':owner_address ,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce_owner
    })
    sign_tx = w3.eth.account.sign_transaction(tx , PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def Awardwinners(address , ID):
    tx = contract.functions.withdrawOwner(address , ID).build_transaction({
        'from':owner_address ,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce_owner
    })
    sign_tx = w3.eth.account.sign_transaction(tx , PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def comptotal(address , ID):
    total = contract.functions.getcomptotal().call()
    return total

def compstatus(address , ID):
    status = contract.functions.getcompstatus().call()
    return status

def compexist(address , ID):
    exist = contract.functions.getcompexist().call()
    return exist