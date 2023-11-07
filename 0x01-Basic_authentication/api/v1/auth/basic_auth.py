#!/usr/bin/env python3
'Baisc auth implemenentation'

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    '''Baisc auth implememntation class'''

    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        '''returns the Base64 part of the Authorization header for a Basic
        Authentication'''
        if authorization_header is None or type(authorization_header) != str:
            return None
        header = authorization_header.split()
        return None if header[0] != 'Basic' else header[1]
        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        '''returns the decoded value of a Base64 string
        base64_authorization_header'''
        if base64_authorization_header is None or \
           type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        '''returns the user email and password from the Base64 decoded value'''
        if decoded_base64_authorization_header is None or \
           type(decoded_base64_authorization_header) != str or \
           ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(':')

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''
        if user_email is None or user_pwd is None or \
           type(user_email) != str or type(user_pwd) != str:
            return None
        try:
            u = User.search({'email': user_email})[0]
        except Exception:
            return None
        if not u:
            return None
        if u.is_valid_password(user_pwd):
            return u
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''overloads Auth and retrieves the User instance for a request'''
        header = self.authorization_header(request)
        if header:
            extracted = self.extract_base64_authorization_header(header)
            u_cred = self.decode_base64_authorization_header(extracted)
            email, pwd = self.extract_user_credentials(u_cred)
            user = self.user_object_from_credentials(email, pwd)
            return user
