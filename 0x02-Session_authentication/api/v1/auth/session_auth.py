#!/usr/bin/env python3
'''session auth'''
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from models.user import User
from typing import TypeVar, Tuple
import uuid


class SessionAuth(Auth):
    '''session auth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
