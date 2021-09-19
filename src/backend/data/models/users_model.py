from src.backend.data.helper import USER_F_NAME, USER_ID, USER_L_NAME, USER_JOIN_DATE, USER_WALLET, USER_PATH_TO_SK, USER_PSEUDO, USER_SUB_TYPE, USER_LAST_PAYED


class User:
    def __init__(self, fname, lname, join_date=None, wallet=None, path_to_sk=None, pseudo=None, sub_type=None, last_payed=None, id=None):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.join_date = join_date
        self.wallet = wallet
        self.path_to_sk = path_to_sk
        self.pseudo = pseudo
        self.sub_type = sub_type
        self.last_payed = last_payed

    def sql_format(self):
        """
        Return object in sql object.

        Return: <dict>
        """
        data = {
            USER_F_NAME: self.fname,
            USER_L_NAME: self.lname,
            USER_JOIN_DATE: self.join_date,
            USER_WALLET: self.wallet,
            USER_PATH_TO_SK: self.path_to_sk,
            USER_PSEUDO: self.pseudo,
            USER_SUB_TYPE: self.sub_type,
            USER_LAST_PAYED: self.last_payed
        }

        if self.id:
            data[USER_ID] = self.id

        return data

    @staticmethod
    def from_sql(row):
        """
        Generate a User from sql.
        """
        return User(
            id=row[USER_ID],
            fname=row[USER_F_NAME],
            lname=row[USER_L_NAME],
            join_date=row[USER_JOIN_DATE],
            wallet=row[USER_WALLET],
            path_to_sk=row[USER_PATH_TO_SK],
            pseudo=row[USER_PSEUDO],
            sub_type=row[USER_SUB_TYPE],
            last_payed=row[USER_LAST_PAYED]
        )