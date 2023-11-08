#!/usr/bin/env python3
'Session auth implementation'

from api.v1.auth.auth import Auth
import os
import uuid


class SessionAuth(Auth):
    '''Session authentiaction class temolate for handling
    session authentication'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None or type(user_id) != str:
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id.update({sess_id: user_id})
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a User ID based on a Session ID'''
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        sess_name = os.getenv('SESSION_NAME')
        return request.cookies.get(sess_name)
