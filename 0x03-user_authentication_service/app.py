#!/usr/bin/env python3
'''flask app'''
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    '''home route'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """POST /users, JSON: -email, -password
    Returns end-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login_session():
    '''login function to respond to the POST /sessions route.'''
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    loggin = AUTH.valid_login(email, password)
    if not loggin:
        abort(401)
    response = make_response(jsonify({
        'email': email,
        'message': 'logged in'
        }))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
