#!/usr/bin/env python3
'Session auth implementation'

from api.v1.auth.auth import Auth
import uuid
from models.user import User


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

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value'''
        cookie_val = self.session_cookie(request)
        u_id = self.user_id_for_session_id(cookie_val)
        return User.get(u_id)

    def destroy_session(self, request=None):
        '''deletes the user session / logout and returns
        bool if success'''
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if not sess_id or not self.user_id_for_session_id(sess_id):
            return False
        if sess_id not in self.user_id_by_session_id:
            return False
        self.user_id_by_session_id.pop(sess_id)
        return True
