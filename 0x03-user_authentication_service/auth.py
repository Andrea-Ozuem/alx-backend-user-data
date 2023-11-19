#!/usr/bin/env python3
'''Password Hashing module'''

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


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

    def create_session(self,  email: str) -> str:
        '''creates a session id for a user'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        u_id = _generate_uuid()
        self._db.update_user(user.id, session_id=u_id)
        return u_id


def _hash_password(password: str) -> bytes:
    '''takes in a password string arguments and returns bytes'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    '''return a string representation of a new UUID'''
    return str(uuid.uuid4())
