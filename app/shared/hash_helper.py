import bcrypt


class HashHelper:

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return (bcrypt.hashpw(salt=salt, password=password.encode())).decode()

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )
