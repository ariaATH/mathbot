from web3 import Web3
from .contract_config import contract_address, contract_abi
import os
from dotenv import load_dotenv

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
OWNER_ADDRESS = os.getenv("OWNER_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

address_node = Web3(Web3.HTTPProvider(RPC_URL))
