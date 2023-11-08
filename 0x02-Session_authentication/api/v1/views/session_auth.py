#!/usr/bin/env python3
""" Module for Session views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_login() -> str:
    '''handles login'''
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not pwd:
        return jsonify({"error": "password missing"}), 400
    u = User.search({'email': email})
    if not u:
        return jsonify({"error": "no user found for this email"}), 404
    u = u[0]
    if not u.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    sess_id = auth.create_session(u.id)
    res = jsonify(u.to_json())
    res.set_cookie(os.getenv('SESSION_NAME'), sess_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def sess_logout() -> str:
    '''Handles user'session logout'''
    from api.v1.app import auth
    deleted = auth.destroy_session(request)
    if deleted is False:
        abort(404)
    return jsonify({}), 200
