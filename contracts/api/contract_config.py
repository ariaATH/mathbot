from .web3_config import address_node
import json

contract_address = address_node.to_checksum_address("write address")
contract_abi = json.loads('ABI')
