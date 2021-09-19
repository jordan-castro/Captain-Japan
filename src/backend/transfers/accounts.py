from src.backend.transfers.base import CryptoBase
from src.backend.data.helper import USERS_TABLE, USER_ID, DbHelper
from src.backend.data.models.users_model import User
from src.backend.utils.private_key_handler import private_key, save_locally


class AccountsManager(CryptoBase):
    def __init__(self, user_id):
        self.public_key = None
        self.private_key = None
        self.user = None
        self.setup_account(user_id)

        super().__init__(False)

    def setup_account(self, user_id):
        """
        Set up an account.
        
        Params:
            - <user_id> the id of the user.
        """
        # Grab user
        db = DbHelper()
        user_query = db.query_specific(USERS_TABLE, where=f"{USER_ID} = {user_id}")
        # Close db
        db.close_db()
        # Check we got user back
        if user_query[0]:
            self.user = User.from_sql(user_query[0])
            # Set up public and private key
            self.public_key = self.user.wallet
            self.private_key = private_key(self.user.path_to_sk)

    def sign_transaction(self, tx):
        """
        Sign a transaction for the current account.
        
        Params:
            - <tx: web3.eth.Transaction> the transaction to sign

        Return: <bool>
        """
        sign_tx = self.node.eth.account.sign_transaction(tx, private_key=self.private_key)
        # Try because it can fail
        try:
            self.node.eth.send_raw_transaction(sign_tx.rawTransaction)
            return True
        except:
            return False

    def nonce(self):
        """
        Grab the account nonce.

        Return <int>
        """
        return self.node.eth.getTransactionCount(self.public_key)