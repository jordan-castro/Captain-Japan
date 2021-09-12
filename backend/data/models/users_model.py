from backend.data.helper import USER_ID, USER_NAME, USER_JOIN_DATE, USER_WALLET, USER_PATH_TO_SK, USER_PSEUDO, USER_SUB_TYPE, USER_LAST_PAYED, DbHelper


class User:
    def __init__(self, name, join_date, wallet, path_to_sk, pseudo, sub_type, last_payed, id=None):
        self.id = id
        self.name = name
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
            USER_NAME: self.name,
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
            name=row[USER_NAME],
            join_date=row[USER_JOIN_DATE],
            wallet=row[USER_WALLET],
            path_to_sk=row[USER_PATH_TO_SK],
            pseudo=row[USER_PSEUDO],
            sub_type=row[USER_SUB_TYPE],
            last_payed=row[USER_LAST_PAYED]
        )