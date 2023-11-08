#!/usr/bin/env python3

'''Auths base class implementaion for auth
'''

from flask import request
from typing import List, TypeVar
import os


class Auth:
    '''a template class to manage the API authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Checks if a path requires authentication'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        '''validate all requests to secure the API
        '''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''
        returns None - request
        '''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        sess_name = os.getenv('SESSION_NAME')
        return request.cookies.get(sess_name)
