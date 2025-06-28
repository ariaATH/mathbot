from web3 import Web3
from .contract_config import contract_address, contract_abi
import os
from dotenv import load_dotenv

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

address_node = Web3(Web3.HTTPProvider(RPC_URL))
w3 = Web3(address_node)
contract = address_node.eth.contract(address=contract_address, abi=contract_abi)

def create_Tx(value , user_address):
  tx = {
    'to' : contract_address,
    'value' : hex(w3.to_wei(value , 'ether')),
    'gas' :  hex(2100),                     
    'gasPrice' :hex(w3.eth.gas_price),
    'nonce' :  w3.eth.get_transaction_count(user_address),
    'chainId' : 56
  }