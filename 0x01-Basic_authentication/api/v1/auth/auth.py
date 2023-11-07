#!/usr/bin/env python3
'Auths base class'

from flask import request
from typing import List, TypeVar


class Auth:
    '''a class to manage the API authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Checks if a path requires authentication'''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path = path + '/'
        return True if path not in excluded_paths else False

    def authorization_header(self, request=None) -> str:
        '''validate all requests to secure the API'''
        head = request.headers.get('Authorization')
        return None if request is None else head

    def current_user(self, request=None) -> TypeVar('User'):
        return None
