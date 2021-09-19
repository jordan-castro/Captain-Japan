# from src.backend.data.helper import USER_F_NAME, USER_ID, USER_L_NAME, USER_PSEUDO, USERS_TABLE, DbHelper
# from src.backend.data.models.users_model import User
# import time


# def signup(fname: str, lname: str, pseudo: str=None):
#     """
#     Create a new USER for Captain Japan.

#     Params:
#         - <fname: str> The user's first name.
#         - <lname: str> The user's last name.
#         - <pseudo: str=None> Kinda like a username.

#     Returns: <User> 
#     """
#     db = DbHelper()
#     # Insert into db
#     user = User(
#         fname=fname,
#         lname=lname,
#         join_date=int(time.time()),
#         pseudo=pseudo
#     )
#     db.insert(USERS_TABLE, user.sql_format())
#     print(f"{USER_F_NAME} = {fname}")
#     # Query the user now
#     user = db.query_specific(USERS_TABLE, where=f"{USER_F_NAME} = '{fname}'", order=f"BY {USER_ID} DESC")[0]
#     # Close db
#     db.close_db()
#     return User.from_sql(user)


# def grab_user(user_id):
#     """
#     Grab the user from the SQL based on their user id.

#     Params:
#         - <user_id: int> The id of the user.

#     Returns: <User|False>
#     """
#     db = DbHelper()
#     # Query
#     user = db.query_specific(USERS_TABLE, where=f"{USER_ID} = {user_id}")[0]
#     # Check for compiler suggestions
#     if not user:
#         return False
#     db.close_db()
#     # Return user data
#     return User.from_sql(user)