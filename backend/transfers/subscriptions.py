from backend.transfers.accounts import AccountsManager
from backend.transfers.base import CryptoBase


class SubscriptionsHandler(CryptoBase):
    def is_subscribed(self, account)-> bool:
        """
        Check if account is subscribed and can download.

        Params:
            - <account: str> The account in question.

        Return: <bool>
        """
        # Check with contract
        return self.contract.functions.subscribed(account).call()

    def is_valid_subscriber(self, account, key)-> bool:
        """
        Validate the subscriber.

        Params:
            - <account: str> The account in question.
            - <key: str> The subscribers SECRET key.

        Return: <bool>
        """
        # Contract call
        return self.contract.functions.validSubscriber(account, key).call()

    def forgot_secret_key(self, account: AccountsManager):
        """
        Get the secret key of the account passed and return it to the user.
        
        Note: <account> comes from the application and can not be manipulated by the user.
        Note: the only way to get the secret key is if the owner of <account> has provided,
        their private key. Otherwise this method will fail.

        Params:
            - <account: AccountsManager> the account to get the key for.

        Return: <str|False>
        """
        # Wrap with try block
        try:
            # transaction data
            tx_data = self.build_transaction_dict(account.nonce(), value=self.forgot_key_fee())
            tx = self.contract.functions.forgotSecretKey().buildTransaction(tx_data)
            # Todo figure out how to return string from smart contract.
        except:
            return False

        return key

    def change_secret_key(self, key):
        pass # ^

    def subscribe(self, account: AccountsManager, sub_type, key):
        """
        Subscribe to CaptainJapan.

        Subscription types:
            - monthly 0.01 BNB
            - quarterly 0.05 BNB
            - halfly (half a year) 0.1 BNB
            - yearly 0.2 BNB

        Note: User has to renew their subscription at the end because the contract does not
        charge automattically. Nor do we want it to.
        Note: <account> comes from the application and can not be manipulated by the user.

        Params:
            - <account: AccountsManager> the account subscribing.
            - <sub_type: int> the type of subscription.
            - <key: str> secret custom key for the contracts KYC. DON'T SHARE!!

        Return: <tuple(bool, end_of_sub: int)>
        """
        try:
            payment_info = self.payment_type_info(sub_type)
            # Build transaction data
            tx_data = self.build_transaction_dict(account.nonce(), value=payment_info[0])
            # Contract call
            tx = self.contract.functions.subscribe(sub_type, key).buildTransaction(tx_data)
            account.sign_transaction(tx)
        except Exception as e:
            print(e)
            return False
        
        # Todo calculate time till (end of subscription)
        return (True, payment_info[1])

    def gift_subscription(self, reciever, sender: AccountsManager, sub_type, key):
        """
        Gift a subscription within CaptainJapan.

        Subscription types:
            - monthly 0.01 BNB
            - quarterly 0.05 BNB
            - halfly (half a year) 0.1 BNB
            - yearly 0.2 BNB

        Note: User has to renew their subscription at the end because the contract does not
        charge automattically. Nor do we want it to.
        Note: <account> comes from the application and can not be manipulated by the user.

        Params:
            - <reciever: str> the account being gifted.
            - <sender: AccountsManager> the account doing the gifting.
            - <sub_type: int> the type of subscription.
            - <key: str> secret custom key for the contracts KYC. The reciever will need this!

        Return <bool>
        """
        try:
            # Build transaction data
            tx_data = self.build_transaction_dict(sender.nonce(), value=self.payment_type_info(sub_type)[0])
            # Contract call
            tx = self.contract.functions.giftSubscription(sub_type, reciever, key).buildTransaction(tx_data)
            sender.sign_transaction(tx)
        except:
            return False

        return True

    def payment_type_info(self, sub_type):
        """
        Get the info for the payment type passed.

        Params:
            - <sub_type: int> The type of subscription in question.

        Return: (price: int, time: int)
        """
        info = self.contract.functions.getPaymentType(sub_type).call()
        # Convert price to Ether
        return (self.node.fromWei(info[0], 'ether'), info[1])

    def forgot_key_fee(self):
        """
        Get the fee for forgetting your secret key.
        """
        fee = self.contract.functions.getForgotKeyFee().call()
        return self.node.fromWei(fee, 'ether')

if __name__ == "__main__":
    crypto = SubscriptionsHandler()
    # Check if is subscribed
    # Run the subscriptions.py script like so
    # brownie run subscriptions
    # Foud in SubscriptionsModel/scripts
    
    # # Testing the subscribe and whatnot
    # account = AccountsManager(1)
    # subscribed = crypto.is_subscribed(account.public_key)
    # if not subscribed:
    #     # Subscribe
    #     crypto.subscribe(account, 0, "Hi")
    
    # subscribed = crypto.is_subscribed(account.public_key)
    # print(subscribed)

    # # Tesing valid user
    # verified = crypto.is_valid_subscriber(account.public_key, "Hi")
    # print(verified)
    
    # Testing gifting/rewards
    account = "0x2FC5f276104aE2D95Bf3F2455D8FB67984F67235"
    sender = AccountsManager(1)
    # crypto.gift_subscription(account, sender, 1, "My friend")

    subscibed = crypto.is_subscribed(account)
    print(subscibed)
    verified = crypto.is_valid_subscriber(account, "My friend")
    print(verified)
    # print(f"Is subscribed {crypto.is_subscribed(crypto.node.eth.accounts[1])}")