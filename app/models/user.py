class User:
    def __init__(self, username: str, hashed_password: str, secret_key: str):
        self.username = username
        self.hashed_password = hashed_password
        self.secret_key = secret_key

        