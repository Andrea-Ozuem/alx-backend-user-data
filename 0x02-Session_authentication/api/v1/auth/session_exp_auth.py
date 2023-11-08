#!/usr/bin/env python3
'Session exp auth implementation'

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import uuid
from models.user import User
import os


class SessionExpAuth(SessionAuth):
    '''add an expiration date to a Session ID'''
    def __init__(self):
        '''Initialise class'''
        self.session_duration = int(os.getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        '''creates a session with expirty date'''
        sess_id = super().create_session(user_id)
        if not sess_id:
            return None
        sess_dict = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id.update({sess_id: sess_dict})
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        '''GEts u_id for a session id
           returns a User ID based on a Session ID'''
        if session_id is None or type(session_id) != str:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')
        created = self.user_id_by_session_id.get(session_id).get('created_at')
        if created is None:
            return None
        if created + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get('user_id')
