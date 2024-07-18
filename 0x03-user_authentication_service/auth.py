#!/usr/bin/env python3
'''auth module'''
import bcrypt
import uuid
from db import DB
from typing import Optional
from user import User
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


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        '''
        takes a single session_id string argument and returns the
        corresponding User or None
        '''
        try:
            current_user = self._db.find_user_by(session_id=session_id)
            return current_user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Takes a single user_id integer srgument
        Returns None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Takes email string argument, Returns string
        Find user corresponding to email, raise ValueError if not exists
        generate uuid and update users reset_token database field
        Return the token if exists
        """
        updated_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=updated_token)
            return updated_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> str:
        """Takes reset_token string argument and a password string
        returns None
        Use reset_token to find corresponding user, raise ValueError
        if doesnt exists, if exists, hash password and update user
        hashed_password field with new hashed password and reset_token
        field to None
        """
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
