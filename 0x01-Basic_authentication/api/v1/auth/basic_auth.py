#!/usr/bin/env python3
'''basic auth'''
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from models.user import User
from typing import TypeVar, Tuple


class BasicAuth(Auth):
    '''basic auth class'''

    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        '''extract's base_64 authorization header'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        base64_part = authorization_header[6:]
        return base64_part

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''decode base64 authorization header'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str

    def extract_user_credentials(
            self, decoded_b64_auth_header: str) -> (str, str):
        """ Returns user credentials """
        if decoded_b64_auth_header is None or not isinstance(
                decoded_b64_auth_header, str) \
           or ':' not in decoded_b64_auth_header:
            return (None, None)
        return decoded_b64_auth_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns user object from credentials """
        if user_email is None or not isinstance(
                user_email, str) or user_pwd is None or not isinstance(
                    user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None