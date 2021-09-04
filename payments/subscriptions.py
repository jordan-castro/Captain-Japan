import web3
from payments.base import CryptoBase


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
        return self.contract.functions.validSubscriber(account, key)

    def forgot_secret_key(self, account)-> bool:
        """
        Get the secret key of the account passed and return it to the user.
        
        Note: <account> comes from the application and can not be manipulated by the user.
        Note: the only way to get the secret key is if the owner of <account> has provided,
        their private key. Otherwise this method will fail.

        Params:
            - <account: str> the account to get the key for.

        Return: <str|False>
        """
        # Wrap with try block
        try:
            key = self.contract.functions.forgotSecretKey({'from': account})
        except:
            return False

        return key

    def change_secret_key(self, key):
        pass # ^

    def subscribe(self, account, sub_type, key):
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
        Note: the only way to get the secret key is if the owner of <account> has provided,
        their private key. Otherwise this method will fail.

        Params:
            - <account: str> the account subscribing.
            - <sub_type: int> the type of subscription.
            - <key: str> secret custom key for the contracts KYC. DON'T SHARE!!

        Return: <tuple(bool, end_of_sub: int)>
        """
        try:
            # Contract call
            res = self.contract.functions.subscribe(sub_type, key).transact({'from': account})
        except:
            return False
        
        # Todo calculate time till (end of subscription)
        return (res,)

    def gift_subscription(self, reciever, sender, sub_type, key):
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
        Note: the only way to get the secret key is if the owner of <account> has provided,
        their private key. Otherwise this method will fail.

        Params:
            - <reciever: str> the account being gifted.
            - <sender: str> the account doing the gifting.
            - <sub_type: int> the type of subscription.
            - <key: str> secret custom key for the contracts KYC. The reciever will need this!

        Return <bool>
        """
        try:
            # Contract call
            res = self.contract.functions.giftSubscription(sub_type, reciever, key).transact({'from': sender})
        except:
            return False

        return res


if __name__ == "__main__":
    crypto = SubscriptionsHandler()
    # Check if is subscribed
    # Run the subscriptions.py script like so
    # brownie run subscriptions
    # Foud in SubscriptionsModel/scripts
    print(f"Is subscribed {crypto.is_subscribed(crypto.node.eth.accounts[1])}")