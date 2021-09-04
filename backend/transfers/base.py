from web3 import Web3
from web3.auto import w3
import json


def read_contract_json():
    """
    Get the contract address and abi from a json file.

    Important: There must be a contract.json file

    Return: <tuple(address: str, abi: str)>
    """
    # For now it uses local but in future this will change
    with open("contract.json", "r") as json_file:
        # Grab address and abi
        data = json.load(json_file)
    
    return (
        data['address'], # As is because it's already a string 
        json.dumps(data['abi']) # Convert list json to string
    )


class CryptoBase:
    def __init__(self, build_contract=True):
        self.node = self.connect_node()
        if build_contract:
            self.contract = self.connect_to_contract()
        self.auto = w3

    def connect_node(self):
        """
        Connect to a blockchain node for Web3 integration.
        
        Return: <Web3HttpProvider> working node connection
        """
        network = "http://127.0.0.1:8545"
        return Web3(Web3.HTTPProvider(network))

    def connect_to_contract(self):
        """
        Connect to the Subscriptions contract.

        Return: <Contract|False>
        """
        # Check if node not connected
        if not self.node.isConnected():
            return False

        # Grab the contract info from JSON
        contract_info = read_contract_json()

        # TRY to connect to contract
        try:
            contract = self.node.eth.contract(address=contract_info[0], abi=contract_info[1])
            return contract
        except:
            return False

    def build_transaction_dict(self, nonce, value=None, gas=None, gas_price=10, chain_id=1337):
        """
        Build the transaction dictionary.

        Params:
            - <nonce: int> the nonce of the account calling the transaction.
            - <value: float=None> the value to send to the smart contract. MUST BE IN ETHER FORMAT.
            - <gas: float=None> the max gas value. If not specified, will estimate for you.
            - <gas_price: int=10> the gas_price to start with, MUST BE in GWEI format.
            - <chain_id: int=1337> the id of the blockchain. Default is BSC fork
        
        Return: <dict>
        """
        transaction_data = {
            'chainId': chain_id,
            'gasPrice': self.node.toWei(gas_price, 'gwei'),
            'nonce': nonce
        }
        # Check for value
        if value:
            transaction_data['value'] = self.node.toWei(value, 'ether')

        # Estimate the gas
        estimate_gas = self.node.eth.estimate_gas(transaction_data)
        # transaction_data['gas'] = gas or int(estimate_gas + ((20 / estimate_gas) * 100))
        transaction_data['gas'] = 1000000

        return transaction_data