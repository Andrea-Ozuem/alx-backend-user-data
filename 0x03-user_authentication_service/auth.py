#!/usr/bin/env python3
'''Password Hashing module'''

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register user with pwd and email'''
        try:
            if self._db.find_user_by(email=email):
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        '''Credentials validation'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)


def _hash_password(password: str) -> bytes:
    '''takes in a password string arguments and returns bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
