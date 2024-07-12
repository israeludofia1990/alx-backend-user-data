#!/usr/bin/env python3
'''session auth'''
from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii
from models.user import User
from typing import TypeVar, Tuple


class session(auth):
    '''session auth'''