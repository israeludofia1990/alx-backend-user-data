#!/usr/bin/env python3
'''auth module'''
import bcrypt
import uuid
from db import DB
from user import Users
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Takes in password string argument
    Returns bytes (salted_hashed)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Returns string repr of a new UUID
    Use uuid module
    """
    return str(uuid.uuid4())


def _generate_uuid() -> str:
    """Returns string repr of a new UUID
    Use uuid module
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Users:
        """Takes mandatory string (email, password) arguments
        Returns a User object
        Raise ValueError if exists
        User <user's email> already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Expect email and password required arguments
        Returns a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            # Convert the hashed_password from string to bytes
            hashed_password_bytes = user.hashed_password.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_bytes):
                return True
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Create a session ID for the user with the given email"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
