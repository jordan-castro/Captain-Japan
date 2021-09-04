from web3 import Web3


ADDRESS = '0x97B7c94a7D511E6a02115CceD507f423f9c30F19'
ABI = '[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor", "name": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "subscriber", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "dateSubscribed", "type": "uint256"}, {"indexed": false, "internalType": "uint256", "name": "_type", "type": "uint256"}], "name": "Subscribed", "type": "event"}, {"inputs": [{"internalType": "address", "name": "_newAdmin", "type": "address"}], "name": "addAdmin", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_newRoler", "type": "address"}, {"internalType": "uint256", "name": "role", "type": "uint256"}], "name": "addRole", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_newOwner", "type": "address"}], "name": "changeOwner", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "key", "type": "string"}], "name": "changeSecretKey", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "forgotSecretKey", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "getHandlerAddress", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_type", "type": "uint256"}], "name": "getPaymentType", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_type", "type": "uint256"}, {"internalType": "address", "name": "subscriber", "type": "address"}, {"internalType": "string", "name": "key", "type": "string"}], "name": "giftSubscription", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "payable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_potentialAdmin", "type": "address"}], "name": "isAdmin", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_potentialOwner", "type": "address"}], "name": "isOwner", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_potentialRoler", "type": "address"}, {"internalType": "uint256", "name": "_roleToCheck", "type": "uint256"}], "name": "isRole", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_toBeRemoved", "type": "address"}], "name": "removeRole", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "renounceRole", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "handlerAddress", "type": "address"}], "name": "setHandlersAddress", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_type", "type": "uint256"}, {"internalType": "uint256", "name": "payment", "type": "uint256"}], "name": "setPaymentType", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "stopBeingOwner", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_type", "type": "uint256"}, {"internalType": "string", "name": "key", "type": "string"}], "name": "subscribe", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "payable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_subscriber", "type": "address"}], "name": "subscribed", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "subscriber", "type": "address"}, {"internalType": "string", "name": "secretKey", "type": "string"}], "name": "validSubscriber", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}]'


class CryptoBase:
    def __init__(self, build_contract=True):
        self.node = self.connect_node()
        if build_contract:
            self.contract = self.connect_to_contract()

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

        # TRY to connect to contract
        try:
            contract = self.node.eth.contract(address=ADDRESS, abi=ABI)
            return contract
        except:
            return False