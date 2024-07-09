#!/usr/bin/env python3
'''basic auth'''
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii


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
